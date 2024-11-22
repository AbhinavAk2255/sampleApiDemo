from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import userSerializer, FranchiseeSerializer
from rest_framework import status
from .models import Franchisee, User
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.


class userRegisterView(APIView):

    def post(self, request):

        data = request.data
        serializer = userSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    
            
            




