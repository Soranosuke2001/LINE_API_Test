from rest_framework import serializers

from .models import (
  S3LineImage,
  S3LineVideo,
  S3LineAudio,
  S3LineFile
)


class S3LineImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = S3LineImage
    fields = [
      "image_id",
      "image_url",
      "user_id",
      "timestamp",
    ]


class S3LineVideoSerializer(serializers.ModelSerializer):
  class Meta:
    model = S3LineVideo
    fields = [
      "video_id",
      "video_url",
      "user_id",
      "timestamp",
    ]


class S3LineAudioSerializer(serializers.ModelSerializer):
  class Meta:
    model = S3LineAudio
    fields = [
      "audio_id",
      "audio_url",
      "user_id",
      "timestamp",
    ]


class S3LineFileSerializer(serializers.ModelSerializer):
  class Meta:
    model = S3LineFile
    fields = [
      "file_id",
      "file_url",
      "user_id",
      "timestamp",
    ]

