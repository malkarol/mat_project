from rest_framework import serializers
from session_handler.models import Participant, Session, SessionResult

class ParticipantSerializer(serializers.ModelSerializer):
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