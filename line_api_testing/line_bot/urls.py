from django.urls import path

import views

app_name = "line_bot"

urlpatterns = [
  path("line/image/", views, name="image"),
]
