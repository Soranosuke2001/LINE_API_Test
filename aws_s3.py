from botocore.exceptions import NoCredentialsError

# Specify the bucket name
# bucket_name = 'your-bucket-name'

def upload_to_s3(s3, file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = file_name

    try:
        s3.upload_file(file_name, bucket, object_name)
        print(f"{file_name} has been uploaded to {bucket}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def download_from_s3(s3, bucket, object_name, file_name):
    """Download a file from an S3 bucket

    :param bucket: Bucket to download from
    :param object_name: S3 object name
    :param file_name: File to download to
    """
    try:
        s3.download_file(bucket, object_name, file_name)
        print(f"{object_name} has been downloaded from {bucket}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

# s3 = "boto3.client()"

# Upload a file
# upload_to_s3(s3, 'test.txt', bucket_name)

# Download a file
# download_from_s3(s3, bucket_name, 'test.txt', 'downloaded_test.txt')
