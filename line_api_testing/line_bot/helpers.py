from datetime import datetime

from django.test import Client

from linebot.v3.exceptions import InvalidSignatureError

from .constants import (
  LINE_ROUTES,
  AWS_ROUTES
)


# Verify the Signature
def verify_signature(request, handler):
  if not request:
    return False

  signature = request.headers['X-Line-Signature']
  body = request.body.decode('utf-8')

  try:
    handler.handle(body, signature)
    return True
  except InvalidSignatureError:
    print("Invalid Signature")
    return False
    

# Check the event type
def construct_url(url_type, event):
  if url_type == 'line':
    if not event['type'] == 'message':
      return None
    
    return LINE_ROUTES[event['message']['type']]
  elif url_type == 's3':
    return AWS_ROUTES[event]


# Change the timestamp to DateTime object
def convert_timestamp(timestamp):
  timestamp_seconds = timestamp / 1000
  dt_obj = datetime.fromtimestamp(timestamp_seconds)

  return dt_obj


# Create filtered data object (image endpoint)
def construct_image_data(data):
  content_provider = data['message']['contentProvider']['type']
  dt_obj = convert_timestamp(data['timestamp'])

  if content_provider == 'line':
    image_url = data['message']['id']
  else:
    image_url = data['message']['contentProvider']['originalContentUrl']

  return {
    "image_url": image_url,
    "content_provider": content_provider,
    "source_type": data['source']['type'],
    "reply_token": data['replyToken'],
    "is_redelivery": data['deliveryContext']['isRedelivery'],
    "user_id": data['source']['userId'],
    "webhook_event_id": data['webhookEventId'],
    "timestamp": dt_obj,
  }


# Forward POST request
def forward_request(url, data):
  client = Client()
  response = client.post(url, data, content_type='application/json')
  return response

