import os

from django.shortcuts import render

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
class WebhookEvent(APIView):
  def post(self, request, format=None):
    verified = helpers.verify_signature(request, handler)

    if not verified:
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    data = request.data
    events = data['events']

    for event in events:
      response = helpers.check_event(request, event)

      if not response:
        return Response(status=status.HTTP_403_FORBIDDEN)
      
      if response == "Incomplete":
        return Response(status=status.HTTP_400_BAD_REQUEST)
      
    return Response(status=status.HTTP_200_OK)
  

class LineImageEvent(APIView):
  def post(self, request, format=None):
    data = request.data
    print("This is the LINE IMAGE EVENT")
    print(data)
    print()

    return Response(status=status.HTTP_200_OK)

