from django.urls import path

from . import views

app_name = "line_bot"

urlpatterns = [
  path("", views.WebhookEvent.as_view(), name="webhook_handler"),
  path("submit/image/", views.LineImageEvent.as_view(), name="image_handler"),
  path("submit/video/", views.LineVideoEvent.as_view(), name="video_handler"),
  path("submit/audio/", views.LineAudioEvent.as_view(), name="audio_handler"),
  path("submit/file/", views.LineFileEvent.as_view(), name="file_handler"),

  path("fetch/images/", views.LineImageFetchEvent.as_view(), name="image_fetch"),
  path("fetch/videos/", views.LineVideoFetchEvent.as_view(), name="video_fetch"),
  path("fetch/audios/", views.LineAudioFetchEvent.as_view(), name="audio_fetch"),
  path("fetch/files/", views.LineFileFetchEvent.as_view(), name="file_fetch"),
]
