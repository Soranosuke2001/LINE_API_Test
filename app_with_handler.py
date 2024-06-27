# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
import logging

from argparse import ArgumentParser
from flask import Flask, request, abort
from dotenv import load_dotenv

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

# AWS API imports
import boto3

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

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)


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
    print(parsed_event)
    print()

    message_id = parsed_event.get('message').get('id')
    print(message_id)


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
