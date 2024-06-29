from datetime import datetime

from linebot.v3.exceptions import InvalidSignatureError

from .constants import ROUTES


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
def check_event(event):
  if not event['type'] == 'message':
    return None
  
  url = ROUTES[event['message']['type']]

  return url


# Change the timestamp to DateTime object
def convert_timestamp(timestamp):
  timestamp_seconds = timestamp / 1000
  dt_obj = datetime.fromtimestamp(timestamp_seconds)

  return dt_obj


# Save to S3 bucket
def upload_s3():
  pass