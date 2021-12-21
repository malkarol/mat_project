from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from  ml_handler.models import MLModel
from ml_handler.serializers import MLModelSerializer

@api_view(['GET', 'POST'])
def ml_models_list(request):
    """
    List all participants, or create new one.
    """
    if request.method == 'GET':
        model_list = MLModel.objects.all()
        serializer = MLModelSerializer(model_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MLModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)