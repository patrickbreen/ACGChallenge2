#!/usr/bin/env python3

CODECOMMIT_REPO_NAME = "ACGChallenge2"

from aws_cdk import core

from pipeline.pipeline_stack import PipelineStack
from pipeline.infra_stack import InfraStack

app = core.App()

infra_stack = InfraStack(app, "InfraStack")

PipelineStack(app, "PipelineDeployingInfraStack",
    lambda_code_etl=infra_stack.lambda_code_etl,
    lambda_code_serve=infra_stack.lambda_code_serve,
    repo_name=CODECOMMIT_REPO_NAME)

app.synth()