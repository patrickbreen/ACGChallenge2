
# Welcome to your CDK Python project!

### Deploy

 - deploy (or update) pipeline - `cdk deploy PipelineDeployingLambdaStack`
 - destroy pipeline - `cdk destroy PipelineDeployingLambdaStack`
 
### Note

- Ya, I do build the lambda stacks AND the pipeline on every commit, but only the lambda stacks are deployed.
- Basically the pipeline *ITSELF* is CI only, and all the other infrastructure is CI/CD
- CDK gurus will understand what I mean, I think...


### TODO

- make data ETL lambda and test it
- make API Gateway with lambda backend to read dynamodb data
- make charts.js webpage and host in s3/cloudfront
- make blog post