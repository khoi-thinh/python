#Lambda function triggered off of Event Bridge and CloudTrail event named RunInstances
# When someone creates an EC2, Lambda function will tag it with name of user who created a long with created date

import boto3
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    print(event)
    username = event['detail']['userIdentity']['principalId'].split(':')[1]
    creation_date = event['detail']['userIdentity']['sessionContext']['attributes']['creationDate']
    instance_id = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
    
    #create tag with key:value for created instance
    ec2_response = ec2.create_tags(
        Resources=[
            instance_id,
        ],
        Tags=[
            {
                'Key': 'Resource Creator',
                'Value': username,
            },
            {
                'Key': 'Creation Date',
                'Value': creation_date
            },
        ],
    )
    
    print(ec2_response)  
