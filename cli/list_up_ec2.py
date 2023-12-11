#List up all EC2 based on OS platform

#!/usr/bin/python3

import boto3
import botocore
import csv

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
ec2_result_dict = {}

linux_platform_details = ["Linux/UNIX", "Red Hat BYOL Linux", "Red Hat Enterprise Linux", "Red Hat Enterprise Linux with HA", "Red Hat Enterprise Linux with SQL Server Standard and HA",
                    "Red Hat Enterprise Linux with SQL Server Enterprise and HA", "Red Hat Enterprise Linux with SQL Server Standard", "Red Hat Enterprise Linux with SQL Server Web",
                    "Red Hat Enterprise Linux with SQL Server Enterprise", "SUSE Linux", "Ubuntu Pro"]
                    
windows_platform_details = ["SQL Server Enterprise", "SQL Server Standard", "SQL Server Web","Windows","Windows BYOL",
                            "Windows with SQL Server Enterprise", "Windows with SQL Server Standard", "Windows with SQL Server Web"]
                    
def list_ec2(platform):
    
    if platform == "windows":
        platform = windows_platform_details
    else:
        platform = linux_platform_details
        
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'platform-details',
                'Values': platform
            },
        ]
    )

    for each_result in response['Reservations']:
        ec2_platform = each_result['Instances'][0]['PlatformDetails']
        tags = each_result['Instances'][0]['Tags']
        for tag in tags:
            if tag['Key'] == 'Name':
                ec2_name = tag['Value']
        ec2_result_dict[ec2_name] = ec2_platform
    
    return ec2_result_dict
    
