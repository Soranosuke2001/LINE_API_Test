from linebot.v3.exceptions import InvalidSignatureError


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
  if event['type'] == 'message' and event['message']['type'] == 'text':
    print('text received')
  else:
    print(f'Message type received was {event['message']['type']}')
  print()