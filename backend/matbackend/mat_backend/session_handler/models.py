from django.db import models
from django.utils import tree
from account.models import User
from ml_handler.models import MLModel
from django.core.validators import int_list_validator

#  Specify a translation string by using the function gettext().
#  It’s convention to import this as a shorter alias, _, to save typing.
from django.utils.translation import gettext_lazy as _

class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    related_session = models.IntegerField(default=0)
    model = models.ForeignKey(MLModel, on_delete = models.CASCADE)
    model_uploaded = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    # local path max on Windows
    local_path = models.CharField(max_length=260, default="")
    global_path = models.CharField(max_length=260,  default="")

class SessionResult(models.Model):
    session_result_id = models.AutoField(primary_key=True)
    local_models_accuracy_json = models.CharField(max_length = 1000, null=True)
    finished = models.BooleanField(default=False)
    global_model = models.ForeignKey(MLModel, on_delete=models.CASCADE)

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=400, null=True)
    founder = models.ForeignKey(Participant, on_delete = models.CASCADE)
    result = models.ForeignKey(SessionResult, on_delete = models.SET_NULL, null=True)
    participants = models.CharField(validators=[int_list_validator], max_length=100, null=True)
    min_num_of_participants = models.IntegerField()
    max_num_of_participants = models.IntegerField()
    actual_num_of_participants = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    creation_date = models.DateField(auto_now_add=True)
    with_test_set = models.BooleanField(default=False)
    test_dataset = models.BinaryField(null=True)

     # setting PricingPlanEnum value
    class PricingPlanEnum(models.IntegerChoices):
        FREE = 0, _('Free')
        PREMIUM = 1, _('Paid')

    pricing_plan = models.IntegerField(
      choices=PricingPlanEnum.choices,
      default=PricingPlanEnum.FREE
    )

    # class LossFunctionEnum(models.IntegerChoices):
    #     CATEGORICAL_CROSSENTROPY = 0, _('Categorical Crossentropy')
    #     SVM_LOSS = 1, _('Support vector machines loss')

    # loss_function = models.IntegerField(
    #     choices = LossFunctionEnum.choices,
    #     default = LossFunctionEnum.CATEGORICAL_CROSSENTROPY
    # )

class StorageFile(models.Model):
    file_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=False)
    path = models.CharField(max_length=200, null=False)
    participant_uploaded = models.ForeignKey(Participant, on_delete = models.CASCADE)
    related_session = models.ForeignKey(Session, on_delete = models.CASCADE)