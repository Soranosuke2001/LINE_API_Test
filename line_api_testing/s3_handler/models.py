from django.db import models


# Create your models here.
class S3LineImage(models.Model):
  image_id = models.CharField(max_length=256)
  image_url = models.CharField(max_length=256)
  user_id = models.CharField(max_length=256)
  timestamp = models.DateTimeField()

  def __str__(self):
    return self.image_id

