from django.urls import path

from . import views

app_name = "line_bot"

urlpatterns = [
  path("", views.SaveLineImage.as_view(), name="image"),
]
