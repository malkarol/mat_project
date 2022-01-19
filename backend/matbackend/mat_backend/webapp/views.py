from django.shortcuts import render
from storages.backends.gcloud import GoogleCloudStorage
from rest_framework import serializers, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from session_handler.models import Session, SessionResult, Participant, StorageFile
from django.core.files.base import ContentFile

storage = GoogleCloudStorage()

@api_view(['POST'])
def upload_weights(request):
    if request.method == 'POST':
        file_object = request.FILES['model_weights']
        session = Session.objects.get(pk=request.data['session_id'])
        print(request.data['session_id'])
        target_path = f'/sessions/session_Id_{session.session_id}/local_weights/' + file_object.name
        path = storage.save(target_path, ContentFile(file_object.read()))
        file = StorageFile.objects.create(name=file_object.name, path=path, related_session=session)
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def upload_many(request):
    if request.method == 'POST':
        file_object = request.FILES['files']
        target_path = f'/common/' + file_object.name
        path = storage.save(target_path, ContentFile(file_object.read()))
        return Response(status=status.HTTP_200_OK)
