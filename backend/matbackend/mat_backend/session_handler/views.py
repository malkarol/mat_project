from types import resolve_bases
from django.shortcuts import render

from django.http import FileResponse, response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from account.models import User
from account.serializers import UserSerializer
from session_handler.models import Session, SessionResult, Participant, StorageFile
from session_handler.serializers import SessionResultSerializer, SessionSerializer, ParticipantSerializer
from django.core.files.base import ContentFile
from storages.backends.gcloud import GoogleCloudStorage

# 1. Session CRUD

@api_view(['GET', 'POST'])
def sessions_list(request):
    """
    List all sessions, or create new one.
    """
    if request.method == 'GET':
        sessions_list = Session.objects.all()
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
    if request.method == 'GET':
        participant = Participant.objects.filter(user__id = pk)
        serializer = ParticipantSerializer(participant, many=True)
        return Response([x['session'] for x in serializer.data])

@api_view(['POST'])
def add_one_participants(request):
    pass

@api_view(['POST'])
def add_many_participants(request):
    """
    List all users, or create a new user.
    """
    if request.method =='POST':
        users = User.objects.filter(username__in=request.data['usernames'])
        participants = []
        for user in users:
            participant = {}
            participant['user'] = user['id']
            participant['session'] = request.data['session']
            participants.append(participant)

        serializer = ParticipantSerializer(data=participants,many=True)
        if serializer.is_valid():
            serializer.save()
            try:
                session = Session.objects.get(pk=request.data['session'])
            except Session.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            sessionTmp = {}
            sessionTmp['id'] = session['id']
            sessionTmp['actual_num_of_participants'] =  session['actual_num_of_participants'] + len(participants)

            serializer = SessionSerializer(session, data=sessionTmp)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_participants_for_session(request,pk):
    if request.method == 'GET':
        participant_list = Participant.objects.filter(session__session_id=pk)
        serializer = ParticipantSerializer(participant_list, many=True)
        users_ids = [x['user'] for x in serializer.data]
        users_list = User.objects.filter(id__in=users_ids)
        serializerUser = UserSerializer(users_list, many=True)
        users_dic = [{'username':x['username'],'usertype': x['user_type'],'user_id': x['id']} for x in serializerUser.data]
        print(users_dic)
        return Response(users_dic)


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
        session_id = pk
        #participant_id = request.data['participant_id']

        file = StorageFile.objects.filter(related_session = session_id).filter(participant_uploaded = 2)[0]
        storage_file = storage.open(file.path, 'rb')

        response = FileResponse(storage_file)
        return response


# 4. File dynamically generated
@api_view(['GET'])
def local_model_detail(request):
    response = FileResponse(content_tyoe = 'text/plain')
    response['Content-Disposition'] = 'attachment; filename= local_model.txt'

    lines =['print("Hello world")\n']

    # Write to Python Script
    response.writelines(lines)
    return response