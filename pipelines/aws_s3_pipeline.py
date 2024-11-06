# Import necessary functions from ETL and utility modules
from etls.aws_etl import connect_to_s3, create_bucket_if_not_exist, upload_to_s3
from utils.constants import AWS_BUCKET_NAME

# Define the upload pipeline function to orchestrate uploading data to S3
def upload_s3_pipeline(ti):
    # Pull the file path from the previous task's return value using XCom
    file_path = ti.xcom_pull(task_ids='reddit_extraction', key='return_value')

    # Connect to S3 using the connect_to_s3 function
    s3 = connect_to_s3()

    # Check if the specified bucket exists; if not, create it
    create_bucket_if_not_exist(s3, AWS_BUCKET_NAME)

    # Upload the file to S3 using the file path and bucket name
    # The S3 file name is derived from the last segment of the local file path
    upload_to_s3(s3, file_path, AWS_BUCKET_NAME, file_path.split('/')[-1])
