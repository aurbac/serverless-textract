import json
import boto3
import os

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    print("boto3 version:"+boto3.__version__)
    #print("botocore version:"+botocore.__version__)

    table_name = os.environ['tableName']
    bucket_name = os.environ['bucketName']

    print(json.dumps(event))

    dynamodb_client = boto3.client("dynamodb")
    textract_client = boto3.client('textract')
    s3_client = boto3.client('s3')

    for sqs_record in event['Records']:
        print(json.dumps(sqs_record))
        body = json.loads(sqs_record["body"])
        
        if "Records" in body:
            for record in body['Records']:
                key_object = record["s3"]["object"]["key"]
                bucket_name = record["s3"]["bucket"]["name"]
                if key_object[-3:]=="jpg" or key_object[-3:]=="png":
                    print("Document")
                    response = textract_client.analyze_document(Document={'S3Object': {'Bucket': bucket_name,'Name': key_object}}, FeatureTypes=['TABLES','FORMS'])
                    print(json.dumps(response))
                    s3_client.put_object(Body=json.dumps(response), Bucket=bucket_name, Key=key_object+'.json')
                    response = dynamodb_client.put_item(
                        TableName=table_name,
                        Item={
                            'key_object': {
                                'S': key_object
                            },
                            'bucket_name': {
                                'S': bucket_name
                            },
                            'size_object': {
                                'N': str(record["s3"]["object"]["size"]),
                            }
                        }
                    )

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """