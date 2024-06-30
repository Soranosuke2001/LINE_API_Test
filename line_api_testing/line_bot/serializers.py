from rest_framework import serializers

from .models import (
  LineImage,
  LineVideo,
  LineAudio,
  LineFile
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


class LineVideoSerializer(serializers.ModelSerializer):
  class Meta:
    model = LineVideo
    fields = [
      "video_url",
      "preview_image_url",
      "duration_ms",
      "content_provider",
      "source_type",
      "reply_token",
      "is_redelivery",
      "user_id",
      "webhook_event_id",
      "timestamp",
    ]    


class LineAudioSerializer(serializers.ModelSerializer):
  class Meta:
    model = LineAudio
    fields = [
      "audio_url",
      "duration_ms",
      "content_provider",
      "source_type",
      "reply_token",
      "is_redelivery",
      "user_id",
      "webhook_event_id",
      "timestamp",
    ]    


class LineFileSerializer(serializers.ModelSerializer):
  class Meta:
    model = LineFile
    fields = [
      "file_url",
      "filename",
      "filesize_bytes",
      "content_provider",
      "source_type",
      "reply_token",
      "is_redelivery",
      "user_id",
      "webhook_event_id",
      "timestamp",
    ]    

