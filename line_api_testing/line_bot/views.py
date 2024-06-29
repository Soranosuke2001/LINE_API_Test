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

    print(filtered_data)

    # {
    #   'type': 'message', 
    #   'message': {
    #     'type': 'image', 
    #     'id': '514745570930196633', 
    #     'quoteToken': 'DU3s8NW8pAic_c030S-sM8YL2UdFvE7lku2JHXGYG44Wt6KAe2rAXST2cqvXbOy7cht_7UAUKRPfXYO5D4YEvxssp2bCjYuIuaabo99ecyXJM6GEr92T6oBUFxz9xEFLoNYEdgAx74yzdXJswxExAw', 
    #     'contentProvider': {
    #       'type': 'line'
    #     }
    #   }, 
    #   'webhookEventId': '01J1HBX3QYXVDEN9TKCYY8T5V9', 
    #   'deliveryContext': {
    #     'isRedelivery': False
    #   }, 
    #   'timestamp': 1719643573555, 
    #   'source': {
    #     'type': 'group', 
    #     'groupId': 'C9f33edb10d267bd53df7099fbbbf7b30', 
    #     'userId': 'U4a22d2c862cf4a9b7ecfeb70d33e8b0c'
    #   }, 
    #   'replyToken': '69800e932d69488f921b8a94e3be46f2', 
    #   'mode': 'active'
    # }

    return Response(status=status.HTTP_200_OK)

