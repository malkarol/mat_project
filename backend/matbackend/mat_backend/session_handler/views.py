from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from session_handler.models import Session, SessionResult, Participant
from session_handler.serializers import SessionResultSerializer, SessionSerializer, ParticipantSerializer


@api_view(['GET', 'POST'])
def sessions_list(request):
    """
    List all sessions, or create a new snippet.
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
