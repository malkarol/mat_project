from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from django.http import HttpResponse
from .models import *
from .serializers import UserSerializer
# Create your views here.


class UsersView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class SessionsView(generics.RetrieveAPIView):
    queryset = Session.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class SessionsResultsView(generics.RetrieveAPIView):
    queryset = SessionResult.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

