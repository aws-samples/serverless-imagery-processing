## Processing satellite imagery with AWS serverless architecture

This repo contains code and Severless Application Model configurations to deploy a serverless imagery processing pipeline in the AWS cloud.


### Install dependencies

In order to deploy this stack automatically [AWS Serverless application Model](https://aws.amazon.com/serverless/sam/) is used.  An AWS account will also be needed in order to deploy the stack within the AWS cloud

### Usage


After cloning the code repository:

Navigate to the repository:
```
cd Imagery-processing-blog
```
Build the AWS SAM application:
```
sam build
```
Deploy the AWS SAM application:
```
sam deploy –guided
```

The current inference engine in the pipeline is Rekognition. This is commented out so you do not incur unexpected costs.  See the blog post for more information, [Processing Imagery with Serverless Architecture](https://aws.amazon.com/blogs/compute/processing-satellite-imagery-with-serverless-architecture/).
### License

This library is licensed under the MIT-0 License. See the LICENSE file.

