import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
  S3LineImageSerializer
)
from .models import (
  S3LineImage
)
from .helpers import get_month

BUCKET_NAME = os.getenv("BUCKET_NAME", None)
AWS_REGION = os.getenv("AWS_REGION", None)


# Create your views here.
class S3ImageUploadEvent(APIView):
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
    print("data saved")

    # convert the binary data to image

    # upload the image to the s3 bucket


    return Response(status=status.HTTP_200_OK)
  
  
  def delete(self, request, *args, **kwargs):
    S3LineImage.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

    