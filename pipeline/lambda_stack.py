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


        # Lambda to do ETL
        self.lambda_code = _lambda.Code.from_cfn_parameters()
        etl_lambda = _lambda.Function(self,'ETL_Lambda',
        handler='lambda-handler.etl',
        runtime=_lambda.Runtime.PYTHON_3_7,
        code=self.lambda_code,
        )
        
        
        # grant permission to lambda to read/write to demo table      
        etl_lambda.add_environment("TABLE_NAME", demo_table.table_name)
        demo_table.grant_write_data(etl_lambda)
        demo_table.grant_read_data(etl_lambda)
        
        
        # Lambda to serve from API Gateway
        self.lambda_code = _lambda.Code.from_cfn_parameters()
        serve_lambda = _lambda.Function(self,'Serve_Lambda',
        handler='lambda-handler.serve',
        runtime=_lambda.Runtime.PYTHON_3_7,
        code=self.lambda_code,
        )
        
        # grant permission to lambda to read/write to demo table      
        serve_lambda.add_environment("TABLE_NAME", demo_table.table_name)
        demo_table.grant_write_data(serve_lambda)
        demo_table.grant_read_data(serve_lambda)
  

        # API Gateway stuff        
        base_api = _apigw.RestApi(self, 'ApiGatewayWithCors',
        rest_api_name='ApiGatewayWithCors')

        example_entity = base_api.root.add_resource('example')
        example_entity_lambda_integration = _apigw.LambdaIntegration(serve_lambda,proxy=False, integration_responses=[
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