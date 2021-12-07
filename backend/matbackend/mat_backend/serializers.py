from rest_framework import serializers

import mat_backend.models as m

class CustomSerializer(serializers.HyperlinkedModelSerializer):

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.User
        fields = '__all__'
        #extra_fields = ['Fullname']

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Participant
        fields = ['ParticipantID','User', 'Session',
        'Model', 'ModelUploaded', 'IsOwner',
        'LocalPath', 'GlobalPath']

class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.MLModel
        fields = ['MLModelID','Name', 'Owner',
        'CreationDate', 'ModelParametersJSON',
        'ModelType']

class SessionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.SessionResult
        fields = ['SessionResultID', 'LocalModelsAccuracyJSON',
        'Finished', 'GlobalModel']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Session
        fields = ['SessionID' 'Name', 'Description','Founder',
        'PricingPlan', 'Result', 'Participants', 'MinNumOfParticipants',
        'MaxNumOfParticipants', 'ActualNumOfParticipants',
        'StartDate', 'EndDate', 'CreationDate', 'WithTestSet',
        'TestDataset']