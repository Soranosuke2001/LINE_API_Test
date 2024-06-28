from django.db import models


# Create your models here.
class LineImage(models.Model):
  image_url = models.CharField(max_length=256)
  content_provider = models.CharField(max_length=10)
  source_type = models.CharField(max_length=10)
  reply_token = models.CharField(max_length=100)
  is_redelivery = models.BooleanField()

  user_id = models.CharField(max_length=256)
  webhook_event_id = models.CharField(max_length=256)

  timestamp = models.DateTimeField()
  received_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.image_url

