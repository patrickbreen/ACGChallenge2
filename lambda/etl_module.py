from urllib import request
import datetime

def get_data(url):
    ftpstream = request.urlopen(url)
    data = ftpstream.read().decode('utf-8')
    return data

# get date -> [cases, deaths]
def extract_nyt(data):
    
    cases = dict()
    exceptions = []
    
    for row in data.split('\n')[1:]:
        try:
            fields = row.split(',')
            date = datetime.datetime.strptime(fields[0], '%Y-%m-%d')
            
            cases[date] = fields[1:]
        
        except Exception as e:
            exceptions.append((row, str(e)))
    return cases, exceptions

    

# get date -> recovered
def extract_jh(data):
    
    recovered = dict()
    exceptions = []
    
    for row in data.split('\n')[1:]:
        try:
            if ',US,' in row:
                fields = row.split(',')
                date_ = datetime.datetime.strptime(fields[0], '%Y-%m-%d')
                recovered_val = fields[-2]
                
                recovered[date_] = recovered_val
        except Exception as e:
            exceptions.append((row, str(e)))
    return recovered, exceptions


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

# load data into dynamodb and send sns notification
def load(dataset, table):
    # The message should include the number of rows updated in the database
    
    number_rows_updated = 0
    exceptions = []
    
    for row in dataset:
        try:
            date_, cases, deaths, recovered = row
            table.put_item(Item={
                'id': date_,
                'cases': int(cases),
                'deaths': int(deaths),
                'recovered': int(recovered),
                
            }, ConditionExpression='attribute_not_exists(date_)')
            number_rows_updated += 1
        except Exception as e:
            exceptions.append((row, str(e)))
    return number_rows_updated, exceptions
