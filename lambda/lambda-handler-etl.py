import csv
import os
import json

import boto3

from etl_module import extract_nyt, extract_jh, get_data, load, merge


# Get the service resource.
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')


# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
table = dynamodb.Table(TABLE_NAME)

    
def handler(event, context):
    
    # Get data from New York Times, and John Hopkins University:
    nytimes_dataset, exceptions_nyt = extract_nyt(get_data('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'))
    hopkins_dataset, exceptions_jh = extract_jh(get_data('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'))
    
    # Combine the two datasets into a single dataset
    combined_dataset = merge(nytimes_dataset, hopkins_dataset)
    
    # Load the dataset into AWS Dynamo Database:
    number_rows_updated, exceptions_load = load(combined_dataset, table)
    
    message = {
        'number_rows_updated': number_rows_updated,
        'exceptions_nyt': len(exceptions_nyt),
        'exceptions_jh': len(exceptions_jh),
        'exceptions_load': len(exceptions_load),
    }
    
    # Send information about success and failure to SNS topic
    response = sns.publish(
        TargetArn=SNS_TOPIC_ARN,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )
    
    # Send information about success and failure as response to this lambda
    return {
        'statusCode': 200,
        'body': message,
    }
    

    

    
