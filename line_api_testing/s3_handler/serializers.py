from rest_framework import serializers

from .models import (
  S3LineImage
)


class S3LineImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = S3LineImage
    fields = [
      "image_id",
      "user_id",
      "timestamp",
    ]

    