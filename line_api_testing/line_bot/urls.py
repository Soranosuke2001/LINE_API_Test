from django.urls import path

from . import views

app_name = "line_bot"

urlpatterns = [
  path("", views.WebhookEvent.as_view(), name="webhook_handler"),
  path("submit/image/", views.LineImageEvent.as_view(), name="image_handler"),
  path("submit/video/", views.LineImageEvent.as_view(), name="video_handler"),
  path("submit/file/", views.LineImageEvent.as_view(), name="file_handler"),
  path("submit/audio/", views.LineImageEvent.as_view(), name="audio_handler"),
]
