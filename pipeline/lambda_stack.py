from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as _apigw,
    aws_dynamodb,
)

class LambdaStack(core.Stack):

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


        # Lambda stuff
        self.lambda_code_etl = _lambda.Code.from_cfn_parameters()
        base_lambda = _lambda.Function(self,'LambdaETL',
            handler='lambda-handler-etl.handler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=self.lambda_code_etl,
        )


        self.lambda_code_serve = _lambda.Code.from_cfn_parameters()
        base_lambda = _lambda.Function(self,'LambdaServe',
            handler='lambda-handler-serve.handler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=self.lambda_code_serve,
        )
  
  
  
        # grant permission to lambda to write to demo table      
        base_lambda.add_environment("TABLE_NAME", demo_table.table_name)
        demo_table.grant_write_data(base_lambda)
        demo_table.grant_read_data(base_lambda)



        # API Gateway stuff        
        base_api = _apigw.RestApi(self, 'ApiGatewayWithCors',
        rest_api_name='ApiGatewayWithCors')

        example_entity = base_api.root.add_resource('example')
        example_entity_lambda_integration = _apigw.LambdaIntegration(base_lambda,proxy=False, integration_responses=[
            {
                'statusCode': '200',
                'responseParameters': {
                'method.response.header.Access-Control-Allow-Origin': "'*'",
                }
            }
                ]
            )
        example_entity.add_method('GET', example_entity_lambda_integration, 
                method_responses=[{
                    'statusCode': '200',
                    'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': True,
                }
            }
        ]
            )

        self.add_cors_options(example_entity)


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