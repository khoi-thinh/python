#Search for EC2s in current region based on a specific tag key:value and take snapshot.

#!/usr/bin/python3

import boto3
import botocore

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
ec2_snapshot_dict = {}
tag_name = "tag:OS"
tag_value = "Windows2019"

ec2_filter_list = ec2.instances.filter(Filters=[
    {
        'Name': tag_name,
        'Values': [tag_value]
    }
    ]
)

for instance in ec2_filter_list:
    volume_list = []
    response = client.describe_tags(
        Filters=[
            {
                'Name': 'resource-id',
                'Values': [
                        instance.id
                    ]
            }
            ])
            
    ec2_name = response['Tags'][1]['Value']
    
    volumes = ec2.Instance(instance.id).volumes.all()
        
    volume_list = [volume.id for volume in volumes]
    
    ec2_snapshot_dict[ec2_name] = volume_list        

for name, volumes in ec2_snapshot_dict.items():
    print(f"Creating snapshot for EC2 instance '{name}'")
    for volume in volumes:
        
        response = client.create_snapshot(
            Description=f"Snapshot of {name}",
            VolumeId=volume)
        
        try:
            snapshot_id = response['SnapshotId']
            waiter = client.get_waiter('snapshot_completed')
            waiter.wait(SnapshotIds=[snapshot_id])
        except botocore.exceptions.WaiterError as e:
            print(e)
    
