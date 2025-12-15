import json
import boto3
from datetime import datetime, timezone, timedelta
import os

# Initialize AWS clients
snsclient = boto3.client('sns')
s3client = boto3.client('s3')
iam_client = boto3.client('iam')


def get_username_from_principal(principal_id):
    """
    Convert principal ID to username using IAM
    """
    try:
        # Extract the user ID from principal (format: AWS:AIDAYG2GDLPHPPJHEGD64)
        if ':' in principal_id:
            user_id = principal_id.split(':')[1]
        else:
            user_id = principal_id
        
        # Query IAM users by UserId
        paginator = iam_client.get_paginator('list_users')
        for page in paginator.paginate():
            for user in page['Users']:
                if user['UserId'] == user_id:
                    return user['UserName']
        
        return f'Unknown ({principal_id})'
        

    except Exception as e:
        # Handle other unexpected errors
        print(f"Unexpected error: {e}")
        return principal_id
    

def lambda_handler(event, context):
    """
    Lambda function triggered by S3 events to send notifications via SNS
    """
    sns_arn = os.environ['sns_topic']
    subject = "S3 Notification"
    try:
        for record in event['Records']:
            # Extract S3 event details
            event_name = record['eventName']
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']
            event_time = record['eventTime']

            # Convert event time to Japan time (JST = UTC+9)
            event_dt = datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%S.%fZ')
            event_dt = event_dt.replace(tzinfo=timezone.utc)
            jst_timezone = timezone(timedelta(hours=9))
            event_time_jst = event_dt.astimezone(jst_timezone).strftime('%Y-%m-%d %H:%M:%S JST')

            # Extract user identity if available
            user_identity = record.get('userIdentity', {})
            principal_id = user_identity.get('principalId', 'Unknown')
            
            # Get username from principal ID
            username = get_username_from_principal(principal_id)

            # Build message
            message = f"""
            ##########################################################
            # File name: {object_key}
            # Person name: {username}
            # Bucket: {bucket_name}
            # Action: {event_name}
            # Date: {event_time_jst}
    
            ##########################################################
            """.strip()

            
            # Send notification to SNS
            response = snsclient.publish(
                TargetArn=sns_arn,
                Subject=subject,
                Message=message
            )
            
            print(f"SNS notification sent! MessageId: {response['MessageId']}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent successfully')
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending notification: {str(e)}')
        }
