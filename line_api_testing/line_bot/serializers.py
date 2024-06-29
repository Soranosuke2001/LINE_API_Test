from rest_framework import serializers

from .models import (
  LineImage
)


class LineImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = LineImage
    fields = [
      "image_url",
      "content_provider",
      "source_type",
      "reply_token",
      "is_redelivery",
      "user_id",
      "webhook_event_id",
      "timestamp",
    ]    

    