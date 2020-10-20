
# First Blog article - Covid data pipeline

I've copied this repository to Github for reference, but it is primarily hosted, and integrated with AWS codedeploy


### Build the Infrastructure locally in development

 - build the pipeline `cdk synthesize PipelineDeployingInfraStackInfraStack`
 - build the other infrastructure `cdk synthesize InfraStack`

### Deploy

- bootstrap the toolset in the region - `cdk bootstrap aws://449614586814/us-east-1`

 - deploy (or update) pipeline - `cdk deploy PipelineDeployingInfraStack`
 - destroy pipeline - `cdk destroy PipelineDeployingInfraStack`
 - destroy other stack - `cdk destroy InfraStack`


### Access the results of the data pipeline:

- Get the raw data output (the actual URL may be different) - `https://wwy7pf7ga7.execute-api.us-east-1.amazonaws.com/prod/api`
- Access the data dashboard - `https://cdk-s3-static-website-blog-pb-2.s3.amazonaws.com/dashboard.html`



 
### Note

- Ya, I do build the lambda stacks AND the pipeline on every commit, but only the lambda stacks are deployed.
- Basically the pipeline *ITSELF* is CI only, and all the other infrastructure is CI/CD
- CDK gurus will understand what I mean, I think...
- Based on my small amount of professional experience, I think that the best practice would be to seperate these things, but this is a toy example anyways.

