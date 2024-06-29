import os
import requests

from django.test import Client
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from linebot.v3 import WebhookHandler

import boto3
from botocore.exceptions import NoCredentialsError

from . import helpers
from .serializers import (
  LineImageSerializer
)
from .models import (
  LineImage
)

CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', None)

handler = WebhookHandler(CHANNEL_SECRET)
S3 = boto3.client('s3')


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class WebhookEvent(APIView):
  def post(self, request, format=None):
    verified = helpers.verify_signature(request, handler)

    if not verified:
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    data = request.data
    events = data['events']

    for event in events:
      url = helpers.check_event(event)

      if not url:
        return Response(status=status.HTTP_403_FORBIDDEN)
      
      response = self.forward_request(reverse(url), event)

      if not response.status_code == 200:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)
  

  def forward_request(self, url, data):
    client = Client()
    response = client.post(url, data, content_type='application/json')
    return response


@method_decorator(csrf_exempt, name='dispatch')
class LineImageEvent(APIView):
  def get(self, request, format=None):
    uploaded_images = LineImage.objects.all()

    serializer = LineImageSerializer(uploaded_images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


  def post(self, request, format=None):
    data = request.data
    content_provider = data['message']['contentProvider']['type']
    dt_obj = helpers.convert_timestamp(data['timestamp'])

    if content_provider == 'line':
      image_url = data['message']['id']
    else:
      image_url = data['message']['contentProvider']['originalContentUrl']

    filtered_data = {
      "image_url": image_url,
      "content_provider": content_provider,
      "source_type": data['source']['type'],
      "reply_token": data['replyToken'],
      "is_redelivery": data['deliveryContext']['isRedelivery'],
      "user_id": data['source']['userId'],
      "webhook_event_id": data['webhookEventId'],
      "timestamp": dt_obj,
    }

    serializer = LineImageSerializer(data=filtered_data)

    if serializer.is_valid():
      serializer.save()
      return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
  

  def delete(self, request, *args, **kwargs):
    LineImage.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

