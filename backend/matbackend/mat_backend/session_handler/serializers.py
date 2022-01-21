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
        fields = ['session_id', 'name', 'description', 'founder', 'min_num_of_participants', 'max_num_of_participants',
        'actual_num_of_participants', 'start_date', 'end_date', 'creation_date', 'parameters_keys', 'parameters_values', 'pricing_plan',
        'tags', 'model_name', 'private_key'
        ]

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageFile
        fields = '__all__'
