from django.urls import path

from . import views

app_name = "line_bot"

urlpatterns = [
  path("", views.WebhookEvent.as_view(), name="webhook-handler"),
  path("image/", views.LineImageEvent.as_view(), name="image-handler"),
  # path("video/", views.LineImageEvent.as_view(), name="video-handler"),
  # path("file/", views.LineImageEvent.as_view(), name="file-handler"),
  # path("audio/", views.LineImageEvent.as_view(), name="audio-handler"),
]
