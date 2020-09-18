from aws_cdk import (core, aws_codebuild as codebuild,
                     aws_codecommit as codecommit,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_lambda as lambda_, aws_s3 as s3)

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, *,
                repo_name: str=None,
                lambda_code_etl: lambda_.CfnParametersCode=None,
                lambda_code_serve: lambda_.CfnParametersCode=None,
                **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        code = codecommit.Repository.from_repository_name(self, "ImportedRepo",
                  repo_name)

        build_pipeline = codebuild.PipelineProject(self, "BuildPipeline",
                        build_spec=codebuild.BuildSpec.from_object(dict(
                            version="0.2",
                            phases=dict(
                                install=dict(
                                    commands=[
                                        "npm install aws-cdk",
                                        "npm update",
                                        "python -m pip install -r requirements.txt"
                                    ]),
                                build=dict(commands=[
                                    "npx cdk synth -o dist"])),
                            artifacts={
                                "base-directory": "dist",
                                "files": [
                                    "InfraStack.template.json"]},
                            environment=dict(buildImage=
                                codebuild.LinuxBuildImage.STANDARD_2_0))))

        build_infra = codebuild.PipelineProject(self, 'BuildInfra',
                        build_spec=codebuild.BuildSpec.from_object(dict(
                            version="0.2",
                            phases=dict(
                                install=dict(
                                    commands=[
                                        "python -m pip install -r requirements.txt"]),
                                ),
                            artifacts={
                                "base-directory": "lambda",
                                "files": [
                                    "lambda-handler-etl.py",
                                    "lambda-handler-serve.py"]},
                            environment=dict(buildImage=
                                codebuild.LinuxBuildImage.STANDARD_2_0))))

        source_output = codepipeline.Artifact()
        build_pipeline_output = codepipeline.Artifact("BuildPipelineOutput")
        build_infra_output = codepipeline.Artifact("BuildInfraOutput")

        infra_location = build_infra_output.s3_location
        
        params = lambda_code_etl.assign(
                bucket_name=infra_location.bucket_name,
                object_key=infra_location.object_key,
                object_version=infra_location.object_version)
                
                
        params.update(
            lambda_code_serve.assign(
                bucket_name=infra_location.bucket_name,
                object_key=infra_location.object_key,
                object_version=infra_location.object_version)
        )

        codepipeline.Pipeline(self, "Pipeline",
            stages=[
                codepipeline.StageProps(stage_name="Source",
                    actions=[
                        codepipeline_actions.CodeCommitSourceAction(
                            action_name="CodeCommit_Source",
                            repository=code,
                            output=source_output)]),
                codepipeline.StageProps(stage_name="Build",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name="Lambda_Build",
                            project=build_infra,
                            input=source_output,
                            outputs=[build_infra_output]),
                        codepipeline_actions.CodeBuildAction(
                            action_name="CDK_Build",
                            project=build_pipeline,
                            input=source_output,
                            outputs=[build_pipeline_output])]),
                codepipeline.StageProps(stage_name="Deploy",
                    actions=[
                        codepipeline_actions.CloudFormationCreateUpdateStackAction(
                            action_name="Infra_CFN_Deploy",
                            template_path=build_pipeline_output.at_path(
                                "InfraStack.template.json"),
                            stack_name="InfraDeploymentStack",
                            admin_permissions=True,
                            parameter_overrides=params,
                            extra_inputs=[build_infra_output])])
                ]
            )