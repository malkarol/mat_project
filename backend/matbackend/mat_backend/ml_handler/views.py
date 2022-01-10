from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from  ml_handler.models import MLModel
from ml_handler.serializers import MLModelSerializer
from session_handler.models import Session
from session_handler.serializers import SessionSerializer
import session_handler.file_finder as ff
import ml_handler.aggregation as agreg


@api_view(['GET', 'POST'])
def ml_models_list(request):
    """
    List all Machine Learning Models, or create new one.
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

@api_view(['GET', 'PUT', 'DELETE'])
def ml_model_detail(request, pk):
    """
    Retrieve, update or delete a Machine Learning Model.
    """
    try:
        ml_model = MLModel.objects.get(pk=pk)
    except MLModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MLModelSerializer(ml_model)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MLModelSerializer(ml_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ml_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def aggregate_on_server(request, pk):
    try:
        session = Session.objects.get(pk=pk)
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SessionSerializer(session)
        if request.user.username == serializer.data['founder']:
            class_name = ff.get_class_name(serializer.data['model_name'])
            zip_iterator = zip(serializer.data['parameters_keys'],serializer.data['parameters_values'])
            parameters= dict(zip_iterator)
            input_size = (32, 32, 3)
            num_of_classes = 10
            # TO DO
            # copy getting files from storage for each list
            client_names = []
            client_counts = []
            global_weights = []
            aggregator = agreg.Aggregator(class_name,input_size,num_of_classes)
            aggregator.get_file_names_and_counts(client_names, client_counts)
            aggregator.aggregate(parameters,client_names,global_weights)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


