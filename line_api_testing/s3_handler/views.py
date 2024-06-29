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
    print('Request received')
    print(request.body)

    return Response(status=status.HTTP_200_OK)

