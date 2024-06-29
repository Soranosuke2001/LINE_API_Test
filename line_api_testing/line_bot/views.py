import os

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
      
      print(f'Before the forward_request: {url}')
      print(f'Sending the following data: {data}')
      print()
      response = self.forward_request(reverse(url), data)

      print()
      print('Completed the forward_request.')
      
    return Response(status=status.HTTP_200_OK)
  
  def forward_request(self, url, data):
    client = Client()
    print("Sending the post request")
    response = client.post(url, data, content_type='application/json')
    print("Completed the post request")


@method_decorator(csrf_exempt, name='dispatch')
class LineImageEvent(APIView):
  def post(self, request, format=None):
    data = request.data
    print("This is the LINE IMAGE EVENT")
    print(data)
    print()

    return Response(status=status.HTTP_200_OK)

