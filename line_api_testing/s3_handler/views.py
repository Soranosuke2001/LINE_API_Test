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
    month_taken = get_month(data['timestamp'])
    image_url = f'https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{user_id}/{month_taken}/{image_id}'

    filtered_data = {

    }

    print("S3 BUCKET")

    # save the image details to the model

    # fetch the image from line data api

    # convert the binary data to image

    # upload the image to the s3 bucket


    return Response(status=status.HTTP_200_OK)

