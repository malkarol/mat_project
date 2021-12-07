from django.db import models
from django.contrib.auth.models import AbstractUser

PRICING_PLANS = [
    (1, 'Registered'),
    (2, 'Premium')
]


USER_TYPES = [
    (0, 'Admin'),
    (1, 'Normal')
]

ML_BACKGROUNDS = [
    (0, 'Student'),
    (1, 'Professor'),
    (2, 'Professional')
]

MODEL_TYPES = [
    (0, 'ImageClassification'),
    (1, 'TextClassification')
]

class User(AbstractUser):
    Fullname = models.CharField(max_length = 30)
    PricingPlan = models.IntegerField(choices=PRICING_PLANS, default = 1)
    UserType = models.IntegerField(choices=USER_TYPES, default = 0)
    MLBackground = models.IntegerField(choices=ML_BACKGROUNDS, default = 0, blank=True)

class Participant(models.Model):
    ParticipantID = models.AutoField(primary_key=True)
    User = models.ForeignKey('User', on_delete = models.CASCADE)
    Session = models.ForeignKey('Session', on_delete = models.CASCADE)
    Model = models.ForeignKey('MLModel', on_delete = models.CASCADE)
    ModelUploaded = models.BooleanField()
    IsOwner = models.BooleanField()
    LocalPath = models.CharField(max_length=400)
    GlobalPath = models.CharField(max_length=400)

class MLModel(models.Model):
    MLModelID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=150)
    Owner = models.ForeignKey('User', on_delete = models.CASCADE)
    CreationDate = models.DateField()
    ModelParametersJSON = models.CharField(max_length=1000)
    ModelType = models.IntegerField(choices=MODEL_TYPES)

class SessionResult(models.Model):
    SessionResultID = models.AutoField(primary_key=True)
    LocalModelsAccuracyJSON = models.CharField(max_length = 1000, null=True)
    Finished = models.BooleanField(default=False)
    GlobalModel = models.ForeignKey('MLModel', on_delete=models.CASCADE)

class Session(models.Model):
    SessionID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200, null=True)
    Description = models.CharField(max_length=400, null=True)
    Founder = models.ForeignKey('Participant', on_delete = models.CASCADE)
    PricingPlan = models.IntegerField(choices=PRICING_PLANS)
    Result = models.ForeignKey('SessionResult', on_delete = models.SET_NULL, null=True)
    Participants = []
    MinNumOfParticipants = models.IntegerField()
    MaxNumOfParticipants = models.IntegerField()
    ActualNumOfParticipants = models.IntegerField()
    StartDate = models.DateField()
    EndDate = models.DateField(null=True)
    CreationDate = models.DateField()
    WithTestSet = models.BooleanField(default=False)
    TestDataset = models.BinaryField(null=True)









