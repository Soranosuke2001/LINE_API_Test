from django.db import models


# Create your models here.
class S3LineImage(models.Model):
  image_id = models.CharField(max_length=256)
  image_url = models.CharField(max_length=256)
  user_id = models.CharField(max_length=256)
  timestamp = models.DateTimeField()

  def __str__(self):
    return self.image_id


class S3LineVideo(models.Model):
  video_id = models.CharField(max_length=256)
  video_url = models.CharField(max_length=256)
  user_id = models.CharField(max_length=256)
  timestamp = models.DateTimeField()

  def __str__(self):
    return self.video_id


class S3LineAudio(models.Model):
  audio_id = models.CharField(max_length=256)
  audio_url = models.CharField(max_length=256)
  user_id = models.CharField(max_length=256)
  timestamp = models.DateTimeField()

  def __str__(self):
    return self.audio_id


class S3LineFile(models.Model):
  file_id = models.CharField(max_length=256)
  file_url = models.CharField(max_length=256)
  user_id = models.CharField(max_length=256)
  timestamp = models.DateTimeField()

  def __str__(self):
    return self.file_id

