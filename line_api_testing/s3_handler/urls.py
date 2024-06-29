from django.urls import path

from . import views

app_name = 's3_handler'

urlpatterns = [
  path("upload/image/", views, name='image_upload'),
  path("upload/video/", views, name='video_upload'),
  path("upload/file/", views, name='file_upload'),
  path("upload/audio/", views, name='audio_upload'),
]
