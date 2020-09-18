import csv
import os

import boto3

from etl_module import extract_nyt, extract_jh, get_data, load, merge


# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)

# init counter if not already exists
# try:
#     table.put_item(Item={'id': 'counter','visitor_count': 0}, ConditionExpression='attribute_not_exists(id)')
# except:
#     pass


# def handler(event, context):
    
#     # use an update expression as an atomic counter
#     item = table.update_item(
#         Key={'id': 'counter'},
#         UpdateExpression="set visitor_count = visitor_count + :val",
#         ExpressionAttributeValues={':val': decimal.Decimal(1)},
#         ReturnValues="UPDATED_NEW")
#     return {
#         'statusCode': 200,
#         'body': {'visitor_count': item['Attributes']['visitor_count']},
#     }

    
def handler(event, context):
    
    nytimes_dataset, exceptions_nyt = extract_nyt(get_data('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'))
    hopkins_dataset, exceptions_jh = extract_jh(get_data('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'))
    combined_dataset = merge(nytimes_dataset, hopkins_dataset)
    
    number_rows_updated, exceptions_load = load(combined_dataset)
    
    # TODO send/failure success to SNS
    return {
        'statusCode': 200,
        'body': {'number_rows_updated': number_rows_updated, 'errors': len(exceptions_load)},
        # 'body': {'combined_dataset': combined_dataset},
    }
    

    

    
