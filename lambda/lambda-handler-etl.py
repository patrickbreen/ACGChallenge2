import csv
from urllib import request
# import os
# import decimal

# import boto3


# # Get the service resource.
# dynamodb = boto3.resource('dynamodb')

# # set environment variable
# TABLE_NAME = os.environ['TABLE_NAME']
# table = dynamodb.Table(TABLE_NAME)

# # init counter if not already exists
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
    nytimes_dataset = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    hopkins_dataset = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'
    
    ftpstream = request.urlopen(url)
    data = ftpstream.read().decode('utf-8')
    
    for row in data.split('\n'):
        print(row)

    
    return {
        'statusCode': 200,
        'body': {'key': row},
    }