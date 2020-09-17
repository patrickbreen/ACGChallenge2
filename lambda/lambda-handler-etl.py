import csv
import datetime
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

# get date -> [cases, deaths]
def extract_nyt(url):
    ftpstream = request.urlopen(url)
    data = ftpstream.read().decode('utf-8')
    
    recovered = dict()
    
    for row in data.split('\n')[1:]:
        fields = row.split(',')
        date = date_time_obj = datetime.datetime.strptime(fields[0], '%Y-%m-%d')
        
        recovered[date] = fields[1:]
        
    return recovered
        
    

# get date -> recovered
def extract_jh(url):
    ftpstream = request.urlopen(url)
    data = ftpstream.read().decode('utf-8')
    
    recovered = dict()
    
    for row in data.split('\n')[1:]:
        if ',US,' in row:
            fields = row.split(',')
            date_ = date_time_obj = datetime.datetime.strptime(fields[0], '%Y-%m-%d')
            recovered_val = fields[-2]
            
            recovered[date_] = recovered_val
    return recovered

# merge New York Times and Johns Hopkins datasets
def merge(nyt_dataset, jh_dataset):
    
    # date, cases, deaths, recovered
    combined_dataset = []
    
    for date_ in nyt_dataset.keys():
        if date_ in jh_dataset:
            row = []
            row.append(str(date_))
            row += nyt_dataset[date_]
            row.append(jh_dataset[date_])
            combined_dataset.append(row)
    return combined_dataset

# TODO load data into dynamodb and send sns notification
def load(dataset):
    # The message should include the number of rows updated in the database
    return 0

    
def handler(event, context):
    

    try:    
        nytimes_dataset = extract_nyt('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
        hopkins_dataset = extract_jh('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')
        combined_dataset = merge(nytimes_dataset, hopkins_dataset)
        
        number_rows_updated = load(combined_dataset)
        
        # TODO send success to SNS
        
        return {
            'statusCode': 200,
            'body': {'key': combined_dataset},
        }
    
    except Exception as e:
        # TODO send failure to SNS
        return {
            'statusCode': 200,
            'body': {'error': e},
        }
    
    

    

    
