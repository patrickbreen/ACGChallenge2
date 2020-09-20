from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as _apigw,
    aws_dynamodb,
    aws_events,
    aws_events_targets,
    aws_sns,
)

from cdk_watchful import Watchful

class InfraStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        # create dynamo table
        demo_table = aws_dynamodb.Table(
            self, "demo_table",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )
        
        # create a Cloudwatch Event rule
        one_day_rule = aws_events.Rule(
            self, "one_day_rule",
            schedule=aws_events.Schedule.rate(core.Duration.days(1)),
        )


        # Lambda stuff
        self.lambda_code_etl = _lambda.Code.from_cfn_parameters()
        lambda_etl = _lambda.Function(self,'LambdaETL',
            handler='lambda-handler-etl.handler',
            timeout=core.Duration.seconds(120),
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=self.lambda_code_etl,
        )
        


        self.lambda_code_serve = _lambda.Code.from_cfn_parameters()
        lambda_serve = _lambda.Function(self,'LambdaServe',
            handler='lambda-handler-serve.handler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=self.lambda_code_serve,
        )
  
  
          # Add target to Cloudwatch Event
        one_day_rule.add_target(aws_events_targets.LambdaFunction(lambda_etl))
  
        # grant permission to lambda to write to demo table      
        lambda_etl.add_environment("TABLE_NAME", demo_table.table_name)
        demo_table.grant_write_data(lambda_etl)
        demo_table.grant_read_data(lambda_etl)
        
        lambda_serve.add_environment("TABLE_NAME", demo_table.table_name)
        demo_table.grant_write_data(lambda_serve)
        demo_table.grant_read_data(lambda_serve)



        # API Gateway stuff        
        base_api = _apigw.RestApi(self, 'ApiGatewayWithCors',
        rest_api_name='ApiGatewayWithCors')

        entity = base_api.root.add_resource('api')
        entity_lambda_integration = _apigw.LambdaIntegration(lambda_serve,proxy=False, integration_responses=[
            {
                'statusCode': '200',
                'responseParameters': {
                'method.response.header.Access-Control-Allow-Origin': "'*'",
                }
            }
                ]
            )
        entity.add_method('GET', entity_lambda_integration, 
                method_responses=[{
                    'statusCode': '200',
                    'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': True,
                }
            }
        ]
            )

        self.add_cors_options(entity)
        
        
        # define a Watchful monitoring system and watch the entire scope
        # this will automatically find all watchable resources and add
        # them to our dashboard
        # I'm not going to put a real email here at this time
        wf = Watchful(self, 'watchful', alarm_email='myemail@email.com')
        wf.watch_scope(self)
        
        # make the SNS resource (called a topic)
        sns_topic = aws_sns.Topic(self, "PipelineTopic")
        lambda_etl.add_environment("SNS_TOPIC_ARN", sns_topic.topic_arn)


    def add_cors_options(self, apigw_resource):
        apigw_resource.add_method('OPTIONS', _apigw.MockIntegration(
            integration_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                    'method.response.header.Access-Control-Allow-Origin': "'*'",
                    'method.response.header.Access-Control-Allow-Methods': "'GET,OPTIONS'"
                }
            }
            ],
            passthrough_behavior=_apigw.PassthroughBehavior.WHEN_NO_MATCH,
            request_templates={"application/json":"{\"statusCode\":200}"}
        ),
        method_responses=[{
            'statusCode': '200',
            'responseParameters': {
                'method.response.header.Access-Control-Allow-Headers': True,
                'method.response.header.Access-Control-Allow-Methods': True,
                'method.response.header.Access-Control-Allow-Origin': True,
                }
            }
        ],
    )