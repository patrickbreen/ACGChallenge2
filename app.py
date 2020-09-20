#!/usr/bin/env python3

CODECOMMIT_REPO_NAME = "ACGChallenge2"

from aws_cdk import core

from pipeline.pipeline_stack import PipelineStack
from pipeline.infra_stack import InfraStack

app = core.App()


# these stacks will be made in my default account and region
env = core.Environment(account="449614586814", region="us-east-1")

infra_stack = InfraStack(app, "InfraStack", env=env)

PipelineStack(app, "PipelineDeployingInfraStack",
    lambda_code_etl=infra_stack.lambda_code_etl,
    lambda_code_serve=infra_stack.lambda_code_serve,
    repo_name=CODECOMMIT_REPO_NAME,
    env=env)

app.synth()