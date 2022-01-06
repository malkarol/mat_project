from django.shortcuts import render

from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
        serializer = ParticipantSerializer(data=request.data)
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