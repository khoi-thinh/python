from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from jira import JIRA
import boto3
from botocore.exceptions import ProfileNotFound, ClientError
import os

app = FastAPI()

# Load environment variables
JIRA_SERVER = os.getenv("JIRA_SERVER")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))

def get_s3_client(profile_name):
    try:
        session = boto3.Session(profile_name=profile_name)
        return session.client('s3')
    except ProfileNotFound:
        return None 

def create_s3_bucket(s3_client, bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
        return False 
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            try:
                s3_client.create_bucket(Bucket=bucket_name)
                print(f"Bucket '{bucket_name}' created successfully.")
                return True
            except ClientError as create_error:
                print(f"Error creating bucket '{bucket_name}': {create_error}")
                return False  
        else:
            print(f"Unexpected error: {e}")
            return False

def process_jira_tickets():
    query_info = 'status = "Building" AND labels = "automated"'
    issues = jira.search_issues(query_info)

    for issue in issues:
        fields = issue.fields
        table_data = fields.description
        parsed_table = parse_jira_table(table_data)
        project_name = parsed_table.get("project_name")
        environment = parsed_table.get("environment")
        bucket_prefix = parsed_table.get("bucket_prefix")

        profile_name = f"{project_name.lower()}_{environment.lower()}"
        s3_client = get_s3_client(profile_name)

        if not s3_client:
            error_message = f"Invalid AWS profile '{profile_name}'."
            jira.add_comment(issue, error_message)
            continue

        bucket_name = f"{bucket_prefix}-{project_name.lower()}-{environment.lower()}"
        if create_s3_bucket(s3_client, bucket_name):
            comment = f"Bucket '{bucket_name}' created successfully."
            jira.add_comment(issue, comment)
        else:
            comment = f"Bucket '{bucket_name}' already exists or there was an error."
            jira.add_comment(issue, comment)

def parse_jira_table(table_data):
    rows = table_data.strip().split("\n")
    parsed_data = {}
    for row in rows:
        if row.startswith("|") and not row.startswith("||"):  
            columns = [col.strip() for col in row.strip("|").split("|")]
            if len(columns) >= 2:
                key, value = columns[0], columns[1]
                parsed_data[key] = value
    return parsed_data

# APScheduler configuration
scheduler = BackgroundScheduler()

# Add a job to check JIRA tickets every minute
scheduler.add_job(process_jira_tickets, "interval", minutes=1)

# Start the scheduler
@app.on_event("startup")
def start_scheduler():
    scheduler.start()

# Shutdown the scheduler on app shutdown
@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
