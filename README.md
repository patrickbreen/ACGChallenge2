
# Welcome to your CDK Python project!

### Deploy

 - deploy (or update) pipeline - `cdk deploy PipelineDeployingInfraStack`
 - destroy pipeline - `cdk destroy PipelineDeployingInfraStack`
 - destroy other stack - `cdk destroy InfraStack`
 
### Note

- Ya, I do build the lambda stacks AND the pipeline on every commit, but only the lambda stacks are deployed.
- Basically the pipeline *ITSELF* is CI only, and all the other infrastructure is CI/CD
- CDK gurus will understand what I mean, I think...


### TODO

- make data ETL lambda and test it
    - send successes and failures to SNS
    - refactor etl code into python module
    - unit tests for success and failure of etl process, and integrate these tests with CI build
- make API Gateway with lambda backend to read dynamodb data
- make charts.js webpage and host in s3/cloudfront
- migrate repo to github and integrate github as a source for CI/CD
- make blog post