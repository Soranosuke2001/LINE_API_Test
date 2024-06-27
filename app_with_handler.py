import os
import sys
import logging
import requests

from dotenv import load_dotenv
from argparse import ArgumentParser

from flask import Flask, request, abort
from PIL import Image
from io import BytesIO

# LINE API imports
from linebot.v3 import (
     WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

from linebot.v3.utils import PY3

# AWS API imports
import boto3
from botocore.exceptions import NoCredentialsError

# Local imports
import aws_s3

load_dotenv()
app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# LINE API Access Tokens
CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', None)
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

if CHANNEL_SECRET is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if CHANNEL_ACCESS_TOKEN is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(CHANNEL_SECRET)

configuration = Configuration(
    access_token=CHANNEL_ACCESS_TOKEN
)

# AWS API Access Tokens
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", None)
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", None)
BUCKET_NAME = os.getenv("BUCKET_NAME", None)

if AWS_ACCESS_KEY is None:
    print('Specify AWS_ACCESS_KEY as environment variable.')
    sys.exit(1)
if AWS_SECRET_KEY is None:
    print('Specify AWS_SECRET_ACCESS_KEY as environment variable.')
    sys.exit(1)
if BUCKET_NAME is None:
    print('Specify BUCKET_NAME as environment variable.')
    sys.exit(1)

s3 = boto3.client('s3')


@app.route("/", methods=["POST"])
def home():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("The signature is not valid")

    return 'OK', 200


@app.route("/test", methods=["GET", "POST"])
def test_message():
    app.logger.info("Testing the info logger")
    app.logger.warning("Testing the warning logger")
    app.logger.debug("Testing the debug logger")
    app.logger.error("Testing the error logger")

    return 'OK', 200


@handler.add(MessageEvent, message=TextMessageContent)
def message_text(event: MessageEvent):
    print(event.to_dict())
    # with ApiClient(configuration) as api_client:
    #     line_bot_api = MessagingApi(api_client)
    #     line_bot_api.reply_message_with_http_info(
    #         ReplyMessageRequest(
    #             reply_token=event.reply_token,
    #             messages=[TextMessage(text=event.message.text)]
    #         )
    #     )


@handler.add(MessageEvent, message=ImageMessageContent)
def message_image(event: MessageEvent):
    parsed_event = event.to_dict()
    message_id = parsed_event.get('message').get('id')

    url = f'https://api-data.line.me/v2/bot/message/{message_id}/content'
    headers = {
    'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            image = Image.open(BytesIO(response.content))
            image_bytes = BytesIO()

            image.save(image_bytes, format="JPEG")
            image_bytes.seek(0)

            aws_s3.upload_to_s3(s3, image_bytes, BUCKET_NAME, "testing")
            print("The image was uploaded successfully")
        except NoCredentialsError:
            print("Error Uploading to S3")
    else:
        print("Unable to fetch the data from LINE API")

    return create_body('OK')


def create_body(text):
    if PY3:
        return [bytes(text, 'utf-8')]
    else:
        return text


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.logger.info("Successfully Started Server")

    # app.run(debug=options.debug, port=options.port, host='0.0.0.0')
    app.run(debug=True, port=options.port, host='0.0.0.0')
