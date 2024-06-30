import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import boto3

from .serializers import (
  S3LineImageSerializer,
  S3LineVideoSerializer,
  S3LineAudioSerializer,
  S3LineFileSerializer,
)
from .models import (
  S3LineImage,
  S3LineVideo,
  S3LineAudio,
  S3LineFile,
)
from .helpers import (
  construct_filtered_data,
  fetch_binary_data,
  binary_image_convert,
  s3_upload
)

s3 = boto3.client('s3')


# Create your views here.
class S3ImageUploadEvent(APIView):
  def post(self, request, format=None):
    filtered_data, image_id, object_path = construct_filtered_data(request.data, 'image')

    # save the image details to the model
    serializer = S3LineImageSerializer(data=filtered_data)

    if not serializer.is_valid():
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()

    # fetch the image from line data api
    response = fetch_binary_data(image_id)

    if not response:
      return Response(status=status.HTTP_401_UNAUTHORIZED)

    # convert the binary data to image
    image = binary_image_convert(response.content)
    
    # upload the image to the s3 bucket
    s3_upload_state = s3_upload(s3, image, object_path, 'image')

    if not s3_upload_state:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)
  
  
  def delete(self, request, *args, **kwargs):
    S3LineImage.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
class S3VideoUploadEvent(APIView):
  def post(self, request, format=None):
    filtered_data, video_id, object_path = construct_filtered_data(request.data, 'video')

    # save the image details to the model
    serializer = S3LineVideoSerializer(data=filtered_data)

    if not serializer.is_valid():
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()

    # fetch the image from line data api
    response = fetch_binary_data(video_id)

    if not response:
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # upload the image to the s3 bucket
    s3_upload_state = s3_upload(s3, response.content, object_path, 'video')

    if not s3_upload_state:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)
  
  
  def delete(self, request, *args, **kwargs):
    S3LineVideo.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
class S3AudioUploadEvent(APIView):
  def post(self, request, format=None):
    filtered_data, audio_id, object_path = construct_filtered_data(request.data, 'audio')

    # save the image details to the model
    serializer = S3LineAudioSerializer(data=filtered_data)

    if not serializer.is_valid():
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()

    # fetch the image from line data api
    response = fetch_binary_data(audio_id)

    if not response:
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # upload the image to the s3 bucket
    s3_upload_state = s3_upload(s3, response.content, object_path, 'audio')

    if not s3_upload_state:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)
  
  
  def delete(self, request, *args, **kwargs):
    S3LineAudio.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
class S3FileUploadEvent(APIView):
  def post(self, request, format=None):
    filtered_data, file_id, object_path = construct_filtered_data(request.data, 'file')

    # save the image details to the model
    serializer = S3LineFileSerializer(data=filtered_data)

    if not serializer.is_valid():
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()

    # fetch the image from line data api
    response = fetch_binary_data(file_id)

    if not response:
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # upload the image to the s3 bucket
    s3_upload_state = s3_upload(s3, response.content, object_path, 'file', response.headers.get('Content-Type'))

    if not s3_upload_state:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)
  
  
  def delete(self, request, *args, **kwargs):
    S3LineFile.objects.all().delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class S3ImageFetchEvent(APIView):
  def get(self, request, format=None):
    s3_images = S3LineImage.objects.all()

    serializer = S3LineImageSerializer(s3_images, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class S3VideoFetchEvent(APIView):
  def get(self, request, format=None):
    s3_videos = S3LineVideo.objects.all()

    serializer = S3LineVideoSerializer(s3_videos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class S3AudioFetchEvent(APIView):
  def get(self, request, format=None):
    s3_audios = S3LineAudio.objects.all()

    serializer = S3LineAudioSerializer(s3_audios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class S3FileFetchEvent(APIView):
  def get(self, request, format=None):
    s3_videos = S3LineFile.objects.all()

    serializer = S3LineFileSerializer(s3_videos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

