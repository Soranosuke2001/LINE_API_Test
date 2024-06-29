import os
import requests
from datetime import datetime

from PIL import Image
from io import BytesIO

from botocore.exceptions import NoCredentialsError

from .constants import MONTH_MAP

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN', None)
IMAGE_FORMAT = os.getenv("IMAGE_FORMAT", "JPEG")


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


# Convert binary image to image
def binary_image_convert(content):
    image = Image.open(BytesIO(content))
    image_bytes = BytesIO()

    image.save(image_bytes, format=IMAGE_FORMAT)
    image_bytes.seek(0)

    return image_bytes


# Fetch the binary image from LINE data API
def fetch_image_binary(image_id):
    url = f'https://api-data.line.me/v2/bot/message/{image_id}/content'
    headers = {
      'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }
    
    response = requests.get(url, headers=headers)

    if not response.status_code == 200:
        return False
    
    return response

