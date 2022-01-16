from rest_framework import serializers
from session_handler.models import Participant, Session, SessionResult, StorageFile

class ParticipantSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField()
    class Meta:
        model = Participant
        fields = '__all__'

class SessionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionResult
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageFile
        fields = '__all__'
