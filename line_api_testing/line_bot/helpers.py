import requests

from django.shortcuts import redirect
from django.http import HttpResponseRedirect

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
def check_event(request, event):
  if not event['type'] == 'message':
    return None
  
  url = ROUTES[event['message']['type']]
  print(f'sending post request to: {url}')
  print()

  return "Complete"
  # url = request.build_absolute_uri(ROUTES[event['message']['type']])
  # url = f'127.0.0.1:8000/{ROUTES[event['message']['type']]}'
  # print(f'sending post request to: {url}')
  # print()
  
  # response = requests.post(url, data=event)
  # print(f"Response: {response}")
  # print()

  # if response.status_code == 200:
  #   return "Complete"
  # else:
  #   return "Incomplete"

