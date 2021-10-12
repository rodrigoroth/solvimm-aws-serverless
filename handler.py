import boto3
import os
from PIL import Image
import json
from boto3.dynamodb.conditions import Key

s3 = boto3.client('s3')


def extract_metadata(event, context):
    print(event)

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    size = event['Records'][0]['s3']['object']['size']
    dynamodb = boto3.client('dynamodb')

    local = '/tmp/' + os.path.basename(key)
    s3.download_file(bucket, key, local)
    im = Image.read(local)
    width, height = im.size

    dynamodb.put_item(
        TableName='serverless-challenge-dev',
        Item={
            's3objectkey': {'S': key},
            'size': {'N': str(size)},
            'height': {'N': str(height)},
            'width': {'N': str(width)}
        })


def get_metadata(event, context):
    dynamodb = boto3.resource('dynamodb')
    # print(event)
    key = event['pathParameters']['s3objectkey']
    data = 'uploads/' + key
    table = dynamodb.Table('serverless-challenge-dev')
    response = table.get_item(
        Key={
            's3objectkey': data
        }
    )
    # print(response)
    return {
        'statusCode': 200,
        'body': response['Item']
    }


def get_image(s3objectkey):
    print("Hello World")


def info_images():
    print("Hello World")


if __name__ == '__main__':
    with open('/home/rodrigo/PycharmProjects/pythonProject/solvimmproject/getdatatempleta.json', 'r') as f:
        template = json.load(f)
    get_metadata(template, "")
