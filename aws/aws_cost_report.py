#!/usr/bin/python3

# Get the cost of each resources up within a date range (from 1st of the current month up to the current time when running the script during that month) and output to CSV file
import boto3
from datetime import date, datetime
import csv

#Cost explorer api
client = boto3.client('ce')

date_format = "%Y-%m-%d"
now = date.today()

current_year = now.year
current_month = now.month
first_day_of_month = "01"

# convert datetime to string format
start_date = "-".join([str(current_year),str(current_month),first_day_of_month])
end_date = datetime.strftime(now, date_format)

# get cost data by services
response = client.get_cost_and_usage(
    TimePeriod={
        'Start': start_date,
        'End': end_date
    },
    Granularity='MONTHLY',
    Metrics=[
        'UnblendedCost'    
    ],
    GroupBy=[
        {
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
        }    
    ])

#narrow down the result
result = response['ResultsByTime'][0]['Groups']

# Save service name and cost in a new dict
final_result = {}

for each in result:
    final_result[each['Keys'][0]] = each['Metrics']['UnblendedCost']['Amount']

#write result to a csv file    
with open('aws_cost_result.csv', 'w', newline='') as my_result:
    writer = csv.writer(my_result)
    for row in final_result.items():
        writer.writerow(row)
    
