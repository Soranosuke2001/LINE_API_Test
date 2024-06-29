from django.urls import path

from . import views

app_name = "line_bot"

urlpatterns = [
  path("", views.WebhookEvent.as_view(), name="webhook_handler"),
  path("image/", views.LineImageEvent.as_view(), name="image_handler"),
  path("video/", views.LineImageEvent.as_view(), name="video_handler"),
  path("file/", views.LineImageEvent.as_view(), name="file_handler"),
  path("audio/", views.LineImageEvent.as_view(), name="audio_handler"),
]
