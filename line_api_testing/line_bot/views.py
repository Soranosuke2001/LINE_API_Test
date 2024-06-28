from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import helpers


# Create your views here.
class SaveLineImage(APIView):
  def post(self, request, format=None):
    verified = helpers.verify_signature(request)

    if not verified:
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    print("Valid signature")

    return Response(status=status.HTTP_200_OK)

