#!/usr/bin/python3

import boto3
import logging, os
from botocore.exceptions import ClientError
from pathlib import Path
from datetime import datetime

# For organizing S3 folders, files will have format such as 2024-10-01/file_name in S3
today_datetime = datetime.now()
formatted_date = today_datetime.strftime('%Y-%m-%d')

local_path = "log_dir_path_here"
target_s3 = "bucket_name_here"

# In this example, grab all .tf files to be uploaded to S3
def get_files(local_path):
    local_path = Path(local_path)
    files = [file_path for file_path in local_path.rglob('*.tf') if file_path.is_file()]
    return files

# upload file function    
def upload_file(file_name, bucket, object_name=None):
    
    s3_client = boto3.client('s3')  
 
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# loop through all file name and call upload function
all_files = get_files(local_path)

for file in all_files:
    upload_file(file,target_s3, '%s/%s' % (formatted_date, file.name))
