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


# Forward POST request
def forward_request(url, data):
  client = Client()
  response = client.post(url, data, content_type='application/json')
  return response


# Save to S3 bucket
def upload_s3():
  pass