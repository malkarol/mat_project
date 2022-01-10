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
import session_handler.file_finder as ff

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
            print(request.data['usernames'])


            session_id = serializer.data['session_id']
            target_path = f'/sessions/session_Id_{session_id}/accuracy_and_loss/'
            path = storage.save(target_path,ContentFile(bytes('', 'utf-8')))
            target_path = f'/sessions/session_Id_{session_id}/local_weights/'
            path = storage.save(target_path,ContentFile(bytes('', 'utf-8')))
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

@api_view(['GET'])
def local_model_script(request):
    file_path = ff.find('CNN',"/common/models/")
    print(file_path)
    storage_file = storage.open(file_path, 'rb')
    print()
    response = FileResponse(storage_file)
    return response

@api_view(['GET'])
def global_model_script(request):
    file_name = 'students.txt'
    lines = []
    data = User.objects.all()
    for d in data:
       lines.append('{0};{1};{2}'.format(d.username,d.email,d.id))
    response_content = '\n'.join(lines)
    response = FileResponse(response_content, content_type="text/plain,charset=utf-8")
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    return response

@api_view(['GET'])
def aggregate_script(request):
    file_name = 'students.txt'
    lines = []
    data = User.objects.all()
    for d in data:
       lines.append('{0};{1};{2}'.format(d.username,d.email,d.id))
    response_content = '\n'.join(lines)
    response = FileResponse(response_content, content_type="text/plain,charset=utf-8")
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    return response
