import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import boto3

from .serializers import (
  S3LineImageSerializer
)
from .models import (
  S3LineImage
)
from .helpers import (
  get_month,
  fetch_image_binary,
  binary_image_convert,
  s3_upload
)

# AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", None)
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
BUCKET_NAME = os.getenv("BUCKET_NAME", None)
AWS_REGION = os.getenv("AWS_REGION", None)

s3 = boto3.client('s3')


# Create your views here.
class S3ImageUploadEvent(APIView):
  def get(self, request, format=None):
    s3_images = S3LineImage.objects.all()

    serializer = S3LineImageSerializer(s3_images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


  def post(self, request, format=None):
    data = request.data

    image_id = data['image_url']
    user_id = data['user_id']
    timestamp, month_taken = get_month(data['timestamp'])
    object_path = f'{user_id}/{month_taken}/{image_id}'
    image_url = f'https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{object_path}'

    filtered_data = {
      "image_id": image_id,
      "image_url": image_url,
      "user_id": user_id,
      "timestamp": timestamp,
    }

    # save the image details to the model
    serializer = S3LineImageSerializer(data=filtered_data)

    if not serializer.is_valid():
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()

    # fetch the image from line data api
    response = fetch_image_binary(image_id)

    if not response:
      return Response(status=status.HTTP_401_UNAUTHORIZED)

    # convert the binary data to image
    image = binary_image_convert(response.content)

    # upload the image to the s3 bucket
    s3_upload_state = s3_upload(s3, image, BUCKET_NAME, object_path)

    if not s3_upload_state:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)
  
  
  def delete(self, request, *args, **kwargs):
    S3LineImage.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

