from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
  S3LineImageSerializer
)
from .models import (
  S3LineImage
)


# Create your views here.
class S3ImageUploadEvent(APIView):
  def post(self, request, format=None):
    data = request.data
    image_id = data['image_url']

    filtered_data = {

    }

    # save the image details to the model

    # fetch the image from line data api

    # convert the binary data to image

    # upload the image to the s3 bucket


    return Response(status=status.HTTP_200_OK)

