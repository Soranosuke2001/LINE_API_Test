import os

from rest_framework.request import Request

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError

CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', None)

handler = WebhookHandler(CHANNEL_SECRET)


# Verify the Signature
def verify_signature(request: Request):
  if not request:
    return False

  signature = request.headers['X-Line-Signature']
  body = request.get_data(as_text=True)

  try:
    handler.handle(body, signature)
    return True
  except InvalidSignatureError:
    print("Invalid Signature")
    return False
    

  