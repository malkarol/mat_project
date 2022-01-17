from os import stat
from types import resolve_bases
from django import http
from django.shortcuts import render
import io
from django.http import HttpResponse
from django.http import FileResponse, response
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from zipfile import *
from django.core.files.storage import default_storage

from account.models import User
from account.serializers import UserSerializer
from session_handler.models import Session, SessionResult, Participant, StorageFile
from session_handler.serializers import SessionResultSerializer, SessionSerializer, ParticipantSerializer, StorageSerializer
from django.core.files.base import ContentFile

from storages.backends.gcloud import GoogleCloudStorage

from django.core.mail import send_mail
import hashlib
from io import BytesIO
import zipfile
from django.http import HttpResponse
import session_handler.file_finder as ff
import ml_handler.aggregation as agreg
from session_handler.ScriptGenerator import ScriptsExecutor

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet_v2 import ResNet50V2
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.applications.mobilenet import MobileNet
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.applications.densenet import DenseNet121
from tensorflow.keras.applications.densenet import DenseNet169
from tensorflow.keras.applications.densenet import DenseNet201
from tensorflow.keras.applications.efficientnet import EfficientNetB0, EfficientNetB1, EfficientNetB2, EfficientNetB3

import inspect

models_dict = {
    'Xception': Xception,
    'VGG19': VGG19,
    'VGG16': VGG16,
    'ResNet50V2': ResNet50V2,
    'ResNet50': ResNet50,
    'MobileNetV2': MobileNetV2,
    'MobileNet': MobileNet,
    'InceptionV3': InceptionV3,
    'InceptionResNetV2': InceptionResNetV2,
    'EfficientNetB0': EfficientNetB0,
    'EfficientNetB1': EfficientNetB1,
    'EfficientNetB2': EfficientNetB2,
    'EfficientNetB3': EfficientNetB3,
    'DenseNet121': DenseNet121,
    'DenseNet169': DenseNet169,
    'DenseNet201': DenseNet201
}


# 3. File upload
storage = GoogleCloudStorage()
# 1. Session CRUD

@api_view(['GET', 'POST'])
def sessions_list(request):
    """
    List all sessions, or create new one.
    """
    if request.method == 'GET':
        sessions_list = Session.objects.all().order_by('-session_id')
        serializer = SessionSerializer(sessions_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def session_detail(request, pk):
    """
    Retrieve, update or delete a Session.
    """
    try:
        session = Session.objects.get(pk=pk)
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SessionSerializer(session)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SessionSerializer(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 2. Participant CRUD
@api_view(['GET', 'POST'])
def participants_list(request):
    """
    List all participants, or create new one.
    """
    if request.method == 'GET':
        participant_list = Participant.objects.all()
        serializer = ParticipantSerializer(participant_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        serializer = ParticipantSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def participant_detail(request, pk):
    """
    Retrieve, update or delete a Participant.
    """
    try:
        participant = Participant.objects.get(pk=pk)
    except Participant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ParticipantSerializer(participant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        participant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_joined_sessions(request,pk):
    '''
    Get list of sessions where logged user is a Participant
    '''
    if request.method == 'GET':
        participant = Participant.objects.filter(user__id = pk)
        serializer = ParticipantSerializer(participant, many=True)
        return Response([x['session'] for x in serializer.data])

@api_view(['GET'])
def get_managed_sessions(request, name):
    '''
    Get list of sessions where logged user is the founder
    '''
    if request.method == 'GET':
        sessionsObjects = Session.objects.filter(founder = name)
        sessions = SessionSerializer(sessionsObjects, many=True)
        return Response(x for x in sessions.data)
@api_view(['GET'])
def get_session_model_progress(request, spk):
    try:
        session = Session.objects.get(pk=spk)
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    participants = Participant.objects.filter(session = session)
    serializer = ParticipantSerializer(participants, many=True)
    return Response(participant for participant in serializer.data)



@api_view(['POST'])
def join_session(request):
    '''
    Creates new participant associated with session
    and rises actual_num_of_participants.
    '''
    try:
        session = Session.objects.get(pk=request.data['session_id'])
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if request.data['private_key'] != '0' and request.data['private_key'] != session.private_key:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sessSerializer = SessionSerializer(session)

        sessionTmp = sessSerializer.data

        sessionTmp['actual_num_of_participants'] =  sessionTmp['actual_num_of_participants'] + 1

        sessSerializer = SessionSerializer(session, data=sessionTmp)
        if sessSerializer.is_valid():
            sessSerializer.save()
            new_data = {}
            new_data['user'] = request.user.id
            new_data['session'] = request.data['session_id']
            new_data['is_owner'] = False
            serializer = ParticipantSerializer(data=new_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(sessSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view('POST')
# def add_filled_session(request):
#     if request.method == 'POST':
#         serializer = SessionSerializer(data=request.data['session'])
#         if serializer.is_valid():
#             serializer.save()
#             usernames = request.data['usernames']
#             users = []
#             for username in usernames:
#                 user = User.objects.get(username=username)
#                 users.append(user)
#             serializerUser = UserSerializer(data=users,many=True)
#             participants = []
#             session_id = serializer.data['session_id']
        #     for user in serializerUser.data:
        #         participant = {}
        #         participant['user'] = user['id']
        #         participant['session'] = session_id
        #         participant['is_owner'] = False
        #         participants.append(participant)

        #     owner ={}
        #     owner['user'] = request.user.id
        #     owner['session'] = session_id
        #     owner['is_owner'] = True
        #     participants.append(owner)

        #     serializerParticipant = ParticipantSerializer(data=participants, many=True)
        #     if serializerParticipant.is_valid():
        #         serializerParticipant.save()
        #         return Response(serializerParticipant.data, status=status.HTTP_201_CREATED)
        # return Response(serializerParticipant.errors, status=status.HTTP_400_BAD_REQUEST)

# def check_if_user_exists(request):
#     usernames = request.data['usernames']
#     users = []
#     for username in usernames:
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         users.append(user)
#     serializerUser =UserSerializer(data=users,many=True)


@api_view(['POST'])
def add_many_participants(request):
    """
    Used when creating session.
    """
    if request.method =='POST':
        users = User.objects.filter(username__in = request.data['usernames'])
        serializerUser = UserSerializer(users,many=True)
        request.data['session']['actual_num_of_participants'] =  request.data['session']['actual_num_of_participants'] + len(users)
        serializer = SessionSerializer(data=request.data['session'])
        if serializer.is_valid():
            serializer.save()
            if serializer.validated_data['pricing_plan'] == Session.PricingPlanEnum.PREMIUM:
                session = Session.objects.get(pk=serializer.data['session_id'])
                send_mail_with_privatekey(session)
                session.save()

            print(request.data['usernames'])


            session_id = serializer.data['session_id']
            target_path = f'/sessions/session_Id_{session_id}/accuracy_and_loss/'
            storage.save(target_path,ContentFile(bytes('', 'utf-8')))
            target_path = f'/sessions/session_Id_{session_id}/local_weights/'
            storage.save(target_path,ContentFile(bytes('', 'utf-8')))

            # input_shape = (28, 28, 1)
            # class_name = serializer.data['model_name']
            # num_classes = 10
            # print(class_name)
            # zip_iterator = zip(serializer.data['parameters_keys'],serializer.data['parameters_values'])
            # parameters= dict(zip_iterator)
            # print("\n\n")
            # print(parameters)
            # print("\n\n")
            # aggregator = agreg.Aggregator(class_name,input_shape,num_classes)
            # global_weights = aggregator.initialize_global_weights(parameters)
            # target_path = f'/sessions/session_Id_{session_id}/global_weights.h5'
            # path = storage.save(target_path, ContentFile(global_weights))
            participants = []
            print("przed valied")
            print(users)

            for user in serializerUser.data:
                participant = {}
                participant['user'] = user['id']
                participant['session'] = session_id
                participant['is_owner'] = False
                participants.append(participant)
            owner ={}
            owner['user'] = request.user.id
            owner['session'] = session_id
            owner['is_owner'] = True
            participants.append(owner)

            print("przed drugim valied")
            serializerParticipant = ParticipantSerializer(data=participants, many=True)
            if serializerParticipant.is_valid():
                serializerParticipant.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_parameters_list_for_model(request, name):
    attributes = inspect.signature(models_dict[name])
    params = dict()
    param_keys = list(attributes.parameters.keys())
    param_values = list(attributes.parameters.values())
    for i in range(len(param_keys)):
        if (param_keys[i] == "kwargs"):
            continue
        params[param_keys[i]] = param_values[i].default
    return Response(params, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_available_models(request):
    return Response(models_dict.keys(), status=status.HTTP_200_OK)



@api_view(['GET'])
def get_results_for_participants(request,pk):
    if request.method == 'GET':
        participant_list = Participant.objects.filter(session__session_id=pk)
        serializer = ParticipantSerializer(participant_list, many=True)
        participants = {}
        losses = []
        names = []
        accuracies = []
        for user in serializer.data:
            losses.append(user['loss'])
            accuracies.append(user['accuracy'])

        users_ids = [x['user'] for x in serializer.data]
        users_list = User.objects.filter(id__in=users_ids)
        serializerUser = UserSerializer(users_list, many=True)
        print()
        for user_2 in users_list:
            names.append(user_2.username)

        participants['names'] = names
        participants['losses'] = losses
        participants['accuracy'] = accuracies

        return Response(participants, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def upload_initial_global_weights(request):
    if request.method == 'POST':
        try:
            print(request.user.id)
            print(request.data['session'])

            session = Session.objects.get(session_id = request.data['session'])
        except Participant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        file_object = request.FILES['files']
        target_path = f'/sessions/session_Id_'+request.data['session']+'/' + 'global_weights.h5'
        if session.founder==request.user.username:
            path = storage.save(target_path, ContentFile(file_object.read()))
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def upload_local_results_json(request):
    try:
       session = Session.objects.get(pk=request.data['session'])
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':

        # participant_list = Participant.objects.filter(session__session_id=request.data['session'])
        # serializerPart = ParticipantSerializer(participant_list, many=True)
        # users_ids = [x['user'] for x in serializerPart.data]
        # if request.user.id in users_ids:
        try:
            participant = Participant.objects.filter(session__session_id=request.data['session']).get(user__id = request.user.id)
        except Participant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        file_object = request.FILES['files']


        content = file_object.read()
        tmpDict = eval(content.decode("utf-8"))
        print(tmpDict)
        participant.accuracy = tmpDict['accuracy']
        participant.loss = tmpDict['loss']
        serializerParticipant = ParticipantSerializer(participant)
        print(serializerParticipant.data)
        participant.save()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_local_weights_json(request):
    try:
       session = Session.objects.get(pk=request.data['session'])
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':

        # participant_list = Participant.objects.filter(session__session_id=request.data['session'])
        # serializerPart = ParticipantSerializer(participant_list, many=True)
        # users_ids = [x['user'] for x in serializerPart.data]
        # if request.user.id in users_ids:
        try:
            participant = Participant.objects.filter(session__session_id=request.data['session']).get(user__id = request.user.id)
        except Participant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        file_object = request.FILES['files']
        session = Session.objects.get(pk=request.data['session'])
        print(file_object.name)
        target_path = f'/sessions/session_Id_{session.session_id}/local_weights/' + file_object.name
        path = storage.save(target_path, ContentFile(file_object.read()))
        file = StorageFile.objects.create(name=file_object.name, path=path, related_session=session)
        # file = StorageFile.objects.create(name=file_object.name, path=path, related_session=session)
        print(file.file_id)
        participant = Participant.objects.filter(session__session_id=request.data['session']).get(user__id = request.user.id)
        serializerParticipant = ParticipantSerializer(participant)
        print(serializerParticipant.data)
        participant.is_model_uploaded = True
        participant.weights_uploaded = file
        participant.local_data_count = int(file.name.split('_')[-1].split('.')[0])
        participant.save()
        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def generate_global_weights(request,pk):
    if request.method == 'GET':
        try:
           session = Session.objects.get(pk=pk)
        except Session.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = SessionSerializer(session)
            if request.user.username == serializer.data['founder']:
                class_name = serializer.data['model_name']
                zip_iterator = zip(serializer.data['parameters_keys'],serializer.data['parameters_values'])
                parameters= dict(zip_iterator)
                parameters['model_name'] = class_name
                parameters['optimizer'] = ff.get_optimizer(parameters['optimizer'])
                lines = ScriptsExecutor().create_initial_weights(parameters)
                print(parameters)
                response_content = '\n'.join(lines)
                response = FileResponse(response_content, content_type="text/plain,charset=utf-8")
                response['Content-Disposition'] = 'attachment; filename=initialize_weights.py'
                return response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_participants_for_session(request,pk):
    if request.method == 'GET':
        participant_list = Participant.objects.filter(session__session_id=pk).order_by('-participant_id')
        serializer = ParticipantSerializer(participant_list, many=True)
        users_ids = [x['user'] for x in serializer.data]
        users_list = User.objects.filter(id__in=users_ids)
        serializerUser = UserSerializer(users_list, many=True)
        users_dic = [{'username':x['username'],'usertype': x['user_type'],'user_id': x['id']} for x in serializerUser.data]
        print(users_dic)
        return Response(users_dic)

@api_view(['DELETE'])
def participant_for_session(request,spk,ppk):
    if (request.method == 'DELETE'):
        try :
            participant = Participant.objects.filter(session_id=spk).filter(user_id=ppk)[0]
            session = Session.objects.get(pk=spk)
            if request.user.id == participant.user_id:
                return Response(status=status.HTTP_403_FORBIDDEN)
            if request.user.username != session.founder:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            participant.delete()
            session.actual_num_of_participants -=  1
            session.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Session.DoesNotExist or Participant.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def leave_session(request, spk):
    if (request.method == 'DELETE'):
        try:
            participant = Participant.objects.filter(session_id=spk).filter(user_id=request.user.id)[0]
            session = Session.objects.get(pk = spk)

            participant.delete()
            session.actual_num_of_participants -=  1
            session.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Participant.DoesNotExist or Session.DoesNotExist or IndexError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# 3. File upload
storage = GoogleCloudStorage()

@api_view(['POST'])
def storage_files_view(request):
    if request.method == 'POST':
        file_object = request.FILES['files']
        session = Session.objects.get(pk=request.data['session_id'])
        target_path = f'/session_Id_{session.session_id}/' + file_object.name
        path = storage.save(target_path, ContentFile(file_object.read()))
        participant = Participant.objects.get(pk=2)
        file = StorageFile.objects.create(name=file_object.name, path=path, participant_uploaded=participant, related_session=session)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def storage_file_detail(request, pk):
    if request.method == 'GET':

        #participant_id = request.data['participant_id']
        participant = Participant.objects.filter(session__session_id=pk).get(user__id = request.user.id)
        file = StorageFile.objects.get(file_id = participant.weights_uploaded_id)
        fileMyname = storage.path(file.name)
        filenames = [fileMyname]

        # Folder name in ZIP archive which contains the above files
        # E.g [thearchive.zip]/somefiles/file2.txt
        # FIXME: Set this to something better
        zip_subdir = "somefiles"
        zip_filename = "%s.zip" % zip_subdir

        response = HttpResponse(content_type='application/zip')
        zip_file = ZipFile(response, 'w')

        for filename in filenames:
            zip_file.write(filename)
        response['Content-Disposition'] = 'attachment; filename={}'.format(zip_filename)
        return response

@api_view(['GET'])
def generate_zip(request,pk):
    list_of_files = StorageFile.objects.all()
    files =[]
    for elem in list_of_files:
        files.append(elem.path)
    zfname = 'somezip.zip'
    # print(list_of_files)
    b =  io.BytesIO()
    with ZipFile(b, 'w') as zf:
            for current_file in list_of_files:
                try:
                    fh = storage.open(current_file.path, "rb")
                    # print(fh.read())
                    zf.writestr(fh.name, fh.read())
                except Exception as e:
                    print(e)
            b.seek(0)
            response = HttpResponse(content_type="application/x-zip-compressed")
            response['Content-Disposition'] = 'attachment; filename={}'.format(zfname)
            # print(b.read())
            response.write(b.read())
            return response




@api_view(['GET'])
def local_model_script(request,pk):
    if request.method == 'GET':
        try:
           session = Session.objects.get(pk=pk)
        except Session.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            participant = Participant.objects.filter(session__session_id=pk).get(user__id = request.user.id)
        except Participant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SessionSerializer(session)
        class_name = serializer.data['model_name']
        zip_iterator = zip(serializer.data['parameters_keys'],serializer.data['parameters_values'])
        parameters= dict(zip_iterator)
        parameters['username'] = request.user.username
        parameters['model_name'] = class_name
        parameters['optimizer'] = ff.get_optimizer(parameters['optimizer'])
        lines = ScriptsExecutor().create_local_model(parameters)
        print(parameters)
        response_content = '\n'.join(lines)
        response = FileResponse(response_content, content_type="text/plain,charset=utf-8")
        response['Content-Disposition'] = 'attachment; filename=initialize_weights.py'
        return response

@api_view(['POST'])
def upload_local_model(request):
    try:
       session = Session.objects.get(pk=request.data['session'])
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':

        # participant_list = Participant.objects.filter(session__session_id=request.data['session'])
        # serializerPart = ParticipantSerializer(participant_list, many=True)
        # users_ids = [x['user'] for x in serializerPart.data]
        # if request.user.id in users_ids:
        try:
            participant = Participant.objects.filter(session__session_id=request.data['session']).get(user__id = request.user.id)
        except Participant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        file_object = request.FILES['files']
        print(type(file_object))
        session = Session.objects.get(pk=request.data['session'])
        target_path = f'/sessions/session_Id_{session.session_id}/local_weigths/' + file_object.name
        path = storage.save(target_path, ContentFile(file_object.read()))
        file = StorageFile.objects.create(name=file_object.name, path=path, related_session=session)
        # file = StorageFile.objects.create(name=file_object.name, path=path, related_session=session)
        print(file.file_id)
        participant = Participant.objects.filter(session__session_id=request.data['session']).get(user__id = request.user.id)
        serializerParticipant = ParticipantSerializer(participant)
        print(serializerParticipant.data)
        participant.is_model_uploaded = True
        participant.weights_uploaded = file
        participant.local_data_count = int(file.name.split('_')[-1].split('.')[0])
        participant.save()
        # print(serializerParticipant.data)


        return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def get_zip(request, pk):
    if request.method == 'GET':
        files = StorageFile.objects.filter(related_session = pk)
        session = Session.objects.get(pk = pk)
        b = BytesIO()

        with zipfile.ZipFile(b, 'w') as zf:
            for file in files:
                try:
                    fh = storage.open(file.path, 'rb')
                    print(fh.name)
                    zf.writestr(f"files/{file.name}", bytes(fh.read()))
                except Exception as e:
                    print(e)
            response = HttpResponse(b.getvalue(), content_type="application/x-zip-compressed")
            response['Content-Disposition'] = f'attachment; filename={session.name}_FILES.zip'
            return response

import tensorflow as tf
@api_view(['GET'])
def test_model(request):
    fh = storage.open('/session_Id_72/hello.h5', 'rb')
    with open("test.h5", 'wb') as f:
        f.write(fh.read())

    model = tf.keras.Sequential()
    model.add(tf.keras.Input(shape=(16,)))
    model.add(tf.keras.layers.Dense(8))

    model.load_weights(fh)
    print(model.get_weights())
    return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
def validate_private_key(request):
    if request.method == 'POST':
        try:
            session = Session.objects.get(private_key=request.data['private_key'])
            return Response(status = status.HTTP_202_ACCEPTED)
        except Session.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

# 4. File dynamically generated
@api_view(['GET'])
def global_model_script(request,pk):
      if request.method == 'GET':
        try:
           session = Session.objects.get(pk=pk)
        except Session.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            participant = Participant.objects.filter(session__session_id=pk).get(user__id = request.user.id)
        except Participant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SessionSerializer(session)

        class_name = serializer.data['model_name']
        zip_iterator = zip(serializer.data['parameters_keys'],serializer.data['parameters_values'])
        parameters= dict(zip_iterator)
        parameters['username'] = request.user.username
        parameters['model_name'] = class_name
        parameters['optimizer'] = ff.get_optimizer(parameters['optimizer'])
        lines = ScriptsExecutor().create_global_model(parameters)
        print(parameters)
        response_content = '\n'.join(lines)
        response = FileResponse(response_content, content_type="text/plain,charset=utf-8")
        response['Content-Disposition'] = 'attachment; filename=global_model_script.py'
        return response

@api_view(['GET'])
def get_global_weights(request,pk):
    path = f'/sessions/session_Id_'+str(pk)+'/' + 'initial_global_weights.h5'
    storage_file = storage.open(path, 'rb')
    response = FileResponse(storage_file)
    return response

@api_view(['GET'])
def get_instructions_local_model(request):
    file_name = 'local_model_instructions.txt'
    text = '''
    ---------- INFORMATION ----------
    1. This set of instructions allows you to run local_model.py file properly.
    Put Python script local_model.py and initial_global_weights.h5 in the same directory as your data folder.
    2. If there is ony one folder with files you can simply run the local_model.py script
    in your favourite IDE, e.g. Visual Studio Code or PyCharm.
    But to run Python script with  the terminal using the following command
    [your python version path] local_model.py [your data set name] \n
    [ EXAMPLE ] python local_model.py data/ \n
    [ REMARK ] Remember to add \ or / at the end of your folder,
    depending if you have Windows or Linux/macOS.
    3. After that '''
    response_content = text
    response = FileResponse(response_content, content_type="text/plain,charset=utf-8")
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response

@api_view(['GET'])
def aggregate_script(request, pk):
    try:
       session = Session.objects.get(pk=pk)
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SessionSerializer(session)
        print("\n\n")
        print(request.user.username)
        print(serializer.data['founder'])
        print("\n\n")
        if request.user.username == serializer.data['founder']:
            class_name = serializer.data['model_name']
            zip_iterator = zip(serializer.data['parameters_keys'],serializer.data['parameters_values'])
            parameters= dict(zip_iterator)
            parameters['username'] = request.user.username
            parameters['model_name'] = class_name
            parameters['optimizer'] = ff.get_optimizer(parameters['optimizer'])
            list_of_participants = Participant.objects.filter(session__session_id = pk)
            username_list = []
            clients_counts = []
            for participant in list_of_participants:
                username_list.append(participant.user.username)
                clients_counts.append(participant.local_data_count)
            parameters['client_names'] = username_list
            parameters['clients_counts'] = clients_counts
            parameters['aggregate_locally'] =  'aggregate_locally'
            lines = ScriptsExecutor().generate_aggregation_script(parameters)
            print(parameters)
            response_content = '\n'.join(lines)
            response = FileResponse(response_content, content_type="text/plain,charset=utf-8")
            response['Content-Disposition'] = 'attachment; filename=initialize_weights.py'
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST)


def send_mail_with_privatekey(session):
    user = User.objects.filter(username = session.founder)[0]
    private_key = generate_private_key(session)
    session.private_key = private_key


    email_body = f"""
NOTE: DO NOT REPLY TO THIS EMAIL, MESSAGE GENERATED AUTOMATICALLY

Dear {user.first_name},
You've just created a new private session: {session.name}
Below you can find your private key. Other people can use it to join your session
PRIVATE KEY: {private_key}

                """
    mail_subject = f"Private key to session: {session.name}"
    send_mail(
        mail_subject,
        email_body,
        'matmailservice@gmail.com',
        recipient_list=[user.email],
        fail_silently=False,
    )


def generate_private_key(session):
    string = str(session.creation_date) + session.name
    encoded = string.encode()
    return hashlib.sha256(encoded).hexdigest()

