from datetime import datetime

from botocore.exceptions import NoCredentialsError

from .constants import MONTH_MAP


# Upload object to s3
def s3_upload(s3, body, bucket_name, object_name):
    try:
        s3.put_object(Bucket=bucket_name, Key=object_name, Body=body, ContentType='image/jpeg')
        print(f"{object_name} has been uploaded to {bucket_name}")
        return True

    except FileNotFoundError:
        print("The file was not found")

    except NoCredentialsError:
        print("Credentials not available")

    except Exception as e:
        print("There was an error: " + e)
    
    return False


# Get the month from datetime object
def get_month(timestamp):
  date_format = "%Y-%m-%dT%H:%M:%S.%f"
  date_object = datetime.strptime(timestamp, date_format)
  month = date_object.month

  return date_object, MONTH_MAP[month]

