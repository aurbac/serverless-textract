# Create a Serverless project to use Textract

Work inside your AWS Cloud9 or local environment.

![serverless-s3-dynamodb](images/serverless-textract.png)

## Configure your environment

``` bash
aws configure
```

- In AWS Cloud9 configure the AWS CLI as follows. 
    - AWS Access Key ID: **(Use default)**
    - AWS Secret Access Key: **(Use default)**
    - Default region name [us-east-1]: **us-east-1**
    - Default output format [json]: **json**
- In your local environment [configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration) with your own IAM credentials.

## Install dependencies

Update Node.js to the minimal version of 8.

``` bash
nvm i v8
```

Install Serverless CLI tool https://serverless.com/framework/docs/providers/aws/guide/installation/

``` bash
npm install -g serverless
```

## Create a Serverless project

``` bash
serverless create --template aws-python --path serverless-textract
cd serverless-textract
echo boto3==1.9.157 > requirements.txt
pip install -r requirements.txt -t .
```

Replace your **handler.py** with the contents of the file [handler.py](handler.py).

Replace your **serverless.yml** with the contents of the file [serverless.yml](serverless.yml), in line **17** is specified the bucket name to be created, change the value for **bucketName** with a unique name (you can use your name or nickname).

## Deploy your Serverless project

``` bash
serverless deploy
```

## Testing

Go to the Amazon S3 Console https://s3.console.aws.amazon.com/, go inside your bucket created and upload a **png** or **jpg** document, few seconds later a json file with the result will be created.

Sample images: [book.zip](files/book.zip)
