from botocore.exceptions import NoCredentialsError

# Specify the bucket name
# bucket_name = 'your-bucket-name'

def upload_to_s3(s3, body, bucket_name, object_name):
    try:
        s3.put_object(Bucket=bucket_name, Key=object_name, Body=body)
        print(f"{object_name} has been uploaded to {bucket_name}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def download_from_s3(s3, bucket_name, object_name, file_name):
    """Download a file from an S3 bucket

    :param bucket: Bucket to download from
    :param object_name: S3 object name
    :param file_name: File to download to
    """
    try:
        s3.download_file(bucket_name, object_name, file_name)
        print(f"{object_name} has been downloaded from {bucket_name}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

# s3 = "boto3.client()"

# Upload a file
# upload_to_s3(s3, 'test.txt', bucket_name)

# Download a file
# download_from_s3(s3, bucket_name, 'test.txt', 'downloaded_test.txt')
