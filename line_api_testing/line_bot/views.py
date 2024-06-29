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
from linebot.v3.webhooks import (
  MessageEvent,
  TextMessageContent,
  ImageMessageContent,
)

from . import helpers
from .serializers import (
  LineImageSerializer
)

CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', None)

handler = WebhookHandler(CHANNEL_SECRET)


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
  def post(self, request, format=None):
    data = request.data

    print('Data Received:')
    print(data)
    print()

    content_provider = data['message']['contentProvider']['type']

    if content_provider == 'line':
      image_url = data['message']['id']
    else:
      image_url = data['message']['contentProvider']['originalContentUrl']

    dt_obj = helpers.convert_timestamp(data['timestamp'])

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
    print('Serializer Data:')
    print(serializer.data)
    print()

    if serializer.is_valid():
      serializer.save()
      print('Saved to DB')
      
      return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


