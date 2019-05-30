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

    for record in event['Records']:
        print(json.dumps(record))
        key_object = record["s3"]["object"]["key"]
        bucket_name = record["s3"]["bucket"]["name"]
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
        if key_object[-3:]=="jpg" or key_object[-3:]=="png" or key_object[-3:]=="pdf":
            print("Document")
            response = textract_client.analyze_document(Document={'S3Object': {'Bucket': bucket_name,'Name': key_object}}, FeatureTypes=['TABLES','FORMS'])
            s3_client.put_object(Body=json.dumps(response), Bucket=bucket_name, Key=key_object+'.json')
            print(json.dumps(response))

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
