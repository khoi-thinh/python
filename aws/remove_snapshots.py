#!/usr/bin/python3

import boto3
from datetime import datetime, timedelta

#Specify the numeber of past days 
number_of_past_days = 1
date_format = "%Y-%m-%d %H:%M:%S.%f%z"
time_now = datetime.now()
past_time = time_now + timedelta(days=-(number_of_past_days))

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

#search for all snapshots, excluding AWS-owned 
snapshots = client.describe_snapshots(OwnerIds=['self'])['Snapshots']

#list up old snapshots based on past time
old_snapshots = [snapshot for snapshot in snapshots if datetime.strftime(snapshot['StartTime'], date_format) < datetime.strftime(past_time,date_format)] 

#remove snapshots
for snapshot in old_snapshots:
    snapshot_id = snapshot['SnapshotId']
    try:
        print(f"Deleting snapshot: {snapshot_id}")
        response = client.delete_snapshot(
            SnapshotId=snapshot_id
        )
    except Exception as e:
        print(f"Error occured when deleting snapshot {snapshot_id}")
        print(e)
