import s3fs
from botocore.exceptions import ClientError
from utils.constants import AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY, AWS_REGION

def connect_to_s3():
    try:
        s3 = s3fs.S3FileSystem(
            key=AWS_ACCESS_KEY_ID,
            secret=AWS_ACCESS_KEY,
            client_kwargs={'region_name': AWS_REGION}
        )
        print('Connected to S3')
        return s3
    except Exception as e:
        print(f"Failed to connect to S3: {e}")
        return None


def create_bucket_if_not_exist(s3, bucket:str, region:str=AWS_REGION):
    try:
        # Check if the bucket already exists
        if not s3.exists(bucket):
            # Create the bucket if it doesn't exist
            s3.mkdir(bucket)
            print("Bucket created")
        else:
            print("Bucket already exists")
    except Exception as e:
        print(f"Error while checking/creating bucket: {e}")


def upload_to_s3(s3, file_path: str, bucket:str, s3_file_name: str):
    try:
        full_path = f"{bucket}/raw_data/{s3_file_name}"
        s3.put(file_path, full_path)
        print(f"File uploaded to s3://{full_path}")
    except FileNotFoundError:
        print('The file was not found')
    except Exception as e:
        print(f"An error occurred: {e}")
