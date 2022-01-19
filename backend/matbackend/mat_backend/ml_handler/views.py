from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from  ml_handler.models import MLModel
from ml_handler.serializers import MLModelSerializer
from account.models import User
from account.serializers import UserSerializer
from session_handler.models import Session, Participant
from session_handler.serializers import SessionSerializer,ParticipantSerializer
import session_handler.file_finder as ff
import ml_handler.aggregation as agreg
from django.core.files.base import ContentFile
from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()

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

            zip_iterator = zip(serializer.data['parameters_keys'],serializer.data['parameters_values'])
            parameters= dict(zip_iterator)
            parameters['model_name'] = ff.get_class_name(serializer.data['model_name'])
            list_of_participants = Participant.objects.filter(session__session_id = pk)
            serializerPar = ParticipantSerializer(list_of_participants , many=True)
            clients_counts = []
            users_ids = [x['user'] for x in serializerPar.data]
            users_list = User.objects.filter(id__in=users_ids)
            serializerUser = UserSerializer(users_list, many=True)
            users_final_list = [[x['username'],x['id']]for x in serializerUser.data]
            participant_final_list = [[x['local_data_count'],x['user']]for x in serializerPar.data]
            users_final_list = sorted(users_final_list, key=lambda x: x[1])
            participant_final_list = sorted(participant_final_list, key=lambda x: x[1])
            print("\n\n")
            print(users_final_list )
            print("\n\n")
            print(participant_final_list)
            print("\n\n")

            parameters['client_names'] =[ x[0] for x in users_final_list ]
            parameters['clients_counts'] = [ x[0] for x in participant_final_list ]
            print(clients_counts)
            width = int(parameters['width_size'])
            height = int(parameters['height_size'])
            num_of_classes =parameters['number_of_classes']
            input_shape = [height,width]
            print("\n\n")
            print(input_shape)
            print("\n\n")
            parameters['optimizer'] = f'tf.keras.optimizers.{parameters["optimizer"]}(learning_rate={parameters["learning_rate"]},momentum={parameters["momentum"]})'
            parameters['model_name'] = ff.get_class_name(serializer.data['model_name'])
            if ff.get_class_name(serializer.data['model_name']) != serializer.data['model_name']:
                print( parameters['model_name'])
                aggregator = agreg.Aggregator(input_shape,num_of_classes,parameters,pk)
            else:
                print( parameters['model_name'])
                aggregator = agreg.PretrainedAggregator(input_shape,num_of_classes,parameters,pk)
            text_path = aggregator.aggregate(parameters)
            file = open(text_path,'rb')
            target_path = f'/sessions/session_Id_{session.session_id}/aggregated_weights.h5'
            path = storage.save(target_path, ContentFile(file.read()))
            file.close()
            os.remove(text_path)
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


