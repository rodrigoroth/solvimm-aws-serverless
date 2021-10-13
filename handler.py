import os
import json
import boto3
from PIL import Image
from collections import Counter

s3 = boto3.client('s3', region_name="us-east-1")
dynamodb = boto3.client('dynamodb', region_name="us-east-1")
resource = boto3.resource('dynamodb', region_name="us-east-1")
table = resource.Table('serverless-challenge-dev')


def extract_metadata(event, context):
    """
    This function invokes a lambda function that access s3 everytime an image is uploaded, then return its metadata
    (key, size, height and width) and stores them on dynamodb serverless-challenge-dev table

    :param event: event source invoked from lambda function that access s3 and return the object metadata
    :type event: object creation
    :param context: lambda function location
    :type context: lambda function
    :return: returns size, height and width from the image uploaded on the database
    :rtype: dict

    """
    key = event['Records'][0]['s3']['object']['key']
    size = event['Records'][0]['s3']['object']['size']

    local = get_image(event)
    im = Image.open(local)
    width, height = im.size

    dynamodb.put_item(
        TableName='serverless-challenge-dev',
        Item={
            's3objectkey': {'S': key},
            'size': {'N': str(size)},
            'height': {'N': str(height)},
            'width': {'N': str(width)}
        })
    return {
        "statusCode": 200,
        "body": {
            "size": str(size),
            "height": str(height),
            "width": str(width)
        }
    }


def get_metadata(event, context):
    """
    This function invokes a lambda function that generates an endpoint for AWS API Gateway created from the s3objectkey
    image uploaded on the database
    
    :param event: event source invoked from lambda function that access dynamodb
    :type event: object response
    :param context: lambda function location
    :type context: lambda function
    :return: returns the metadata from the item stored on the database
    :rtype: dict
    """
    key = event['pathParameters']['s3objectkey']
    data = 'uploads/' + key
    response = table.get_item(
        Key={
            's3objectkey': data
        }
    )
    print(response['Item'])
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        's3objectkey': response['Item']
    }


def get_image(s3objectkey):
    """
    This function receives the s3objectkey from the lambda function extract_metadata event and downloads it so it can
    have its metadata extracted
    
    :param s3objectkey: key used to identify the image uploaded on s3 so it can be downloaded temporarily
    :type s3objectkey: str
    :return: returns the local where the image is temporarily downloaded
    :rtype: str
    """
    bucket = s3objectkey['Records'][0]['s3']['bucket']['name']
    key = s3objectkey['Records'][0]['s3']['object']['key']

    local = os.path.join('/tmp/', os.path.basename(key))
    s3.download_file(bucket, key, local)
    return local


def info_images():
    """
    This function scans the table from dynamodb
    
    :return: returns the biggest and smallest size from all items, the total amount of items and all the items different
    types
    :rtype: dict
    """
    all_items = []
    result_data = table.scan()
    all_items.extend(result_data['Items'])
    while 'LastEvaluatedKey' in result_data:
        result_data = table.scan(ExclusiveStartKey=result_data['LastEvaluatedKey'])
        all_items.extend(result_data['Items'])

    size_list = [int(obj["size"]) for obj in all_items]
    type_list = [obj["s3objectkey"].split(".")[-1] for obj in all_items]
    max_size = max(size_list)
    min_size = min(size_list)
    item_count = len(size_list)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'result': {
            "max_size": max_size,
            "min_size": min_size,
            "item_count": item_count,
            "type_count": dict(Counter(type_list))
        }
    }


if __name__ == '__main__':
    result = info_images()
    print(result)
