from django.urls import path

from . import views

app_name = "line_bot"

urlpatterns = [
  path("", views.WebhookEvent.as_view(), name="webhook-handler"),
]
