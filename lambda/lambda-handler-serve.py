import csv
import os
import json

import boto3

from etl_module import extract_nyt, extract_jh, get_data, load, merge


# Get the service resource.
dynamodb = boto3.resource('dynamodb')


# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)


def handler(event, context):
    items = table.scan()['Items']
    return {
        'statusCode': 200,
        'body': {'data': items},
    }
