import os

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from linebot.v3 import WebhookHandler

from . import helpers
from .serializers import (
  LineImageSerializer
)
from .models import (
  LineImage
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
      url = helpers.construct_url('line', event)

      if not url:
        return Response(status=status.HTTP_404_NOT_FOUND)
      
      response = helpers.forward_request(reverse(url), event)

      if not response.status_code == 200:
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    return Response(status=status.HTTP_200_OK)


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

      # send post request to s3_handler app
      url = helpers.construct_url('s3', data['message']['type'])

      if not url:
        return Response(status=status.HTTP_404_NOT_FOUND)

      response = helpers.forward_request(reverse(url), filtered_data)

      if response.status_code == 200:
        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


  def delete(self, request, *args, **kwargs):
    LineImage.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

