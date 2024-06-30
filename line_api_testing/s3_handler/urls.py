from django.urls import path

from .views import (
  S3ImageUploadEvent,
  S3VideoUploadEvent,
  S3AudioUploadEvent,
  S3FileUploadEvent,

  S3ImageFetchEvent,
  S3VideoFetchEvent,
  S3AudioFetchEvent,
  S3FileFetchEvent,
)

app_name = 's3_handler'

urlpatterns = [
  path("upload/image/", S3ImageUploadEvent.as_view(), name='image_upload'),
  path("upload/video/", S3VideoUploadEvent.as_view(), name='video_upload'),
  path("upload/audio/", S3AudioUploadEvent.as_view(), name='audio_upload'),
  path("upload/file/", S3FileUploadEvent.as_view(), name='file_upload'),
  
  path("fetch/image/", S3ImageFetchEvent.as_view(), name='image_fetch'),
  path("fetch/video/", S3VideoFetchEvent.as_view(), name='video_fetch'),
  path("fetch/audio/", S3AudioFetchEvent.as_view(), name='audio_fetch'),
  path("fetch/file/", S3FileFetchEvent.as_view(), name='file_fetch'),
]
