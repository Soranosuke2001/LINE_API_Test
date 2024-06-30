from django.urls import path

from .views import (
  S3ImageUploadEvent,
  S3VideoUploadEvent,
  S3AudioUploadEvent,
  S3FileUploadEvent,
)

app_name = 's3_handler'

urlpatterns = [
  path("upload/image/", S3ImageUploadEvent.as_view(), name='image_upload'),
  path("upload/video/", S3VideoUploadEvent.as_view(), name='video_upload'),
  path("upload/audio/", S3AudioUploadEvent.as_view(), name='audio_upload'),
  path("upload/file/", S3FileUploadEvent.as_view(), name='file_upload'),
]
