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
