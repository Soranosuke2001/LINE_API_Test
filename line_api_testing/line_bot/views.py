from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class SaveLineImage(APIView):
  def post(self, request, format=None):
    print(request.data)

    return Response(status=status.HTTP_200_OK)

