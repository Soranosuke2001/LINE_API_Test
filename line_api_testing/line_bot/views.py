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
    print(f'Received the following data:')
    print(data)
    print()

    # filtered_data = {}

    # {
    #   'destination': 'U11435cf1030c3004438fad38cdc07ea2', 
    #   'events': [
    #     {
    #       'type': 'message', 
    #       'message': {
    #         'type': 'image', 
    #         'id': '514723178850026160', 
    #         'quoteToken': '_9OcuRCkdQjfam_TQVqc0KjCORs09jeyhCpvMeWymikTWLAE7qatBJEtIGQpayWLCggvVCkbznaHYfrGDJKPFQc54_4FSzMQYkXAJpAf_KRohkcMuC_ubbCIDtX-1uR8Nkilp1uTfU3mlPBxaEDD8g', 
    #         'contentProvider': {
    #           'type': 'line'
    #         }
    #       }, 
    #       'webhookEventId': '01J1GZ5SKZJR97VSBGJY3P5BDX', 
    #       'deliveryContext': {
    #         'isRedelivery': False
    #       }, 
    #       'timestamp': 1719630226991, 
    #       'source': {
    #         'type': 'group', 
    #         'groupId': 'C9f33edb10d267bd53df7099fbbbf7b30', 
    #         'userId': 'U4a22d2c862cf4a9b7ecfeb70d33e8b0c'
    #       }, 
    #       'replyToken': 'acba536a95f54bbe91b3546090fcf020', 
    #       'mode': 'active'
    #     }
    #   ]
    # }

    return Response(status=status.HTTP_200_OK)

