#!/usr/bin/env python3

CODECOMMIT_REPO_NAME = "ACGChallenge2"

from aws_cdk import core

from pipeline.pipeline_stack import PipelineStack
from pipeline.lambda_stack import LambdaStack

app = core.App()

lambda_stack = LambdaStack(app, "LambdaStack")

PipelineStack(app, "PipelineDeployingLambdaStack",
    lambda_code_etl=lambda_stack.lambda_code_etl,
    lambda_code_serve=lambda_stack.lambda_code_serve,
    repo_name=CODECOMMIT_REPO_NAME)

app.synth()