from linebot.v3.exceptions import InvalidSignatureError

# Verify the Signature
def verify_signature(request):
  if not request:
    return False

  signature = request.headers['X-Line-Signature']
  body = request.data

  print(signature)
  print(body)

  return True
  