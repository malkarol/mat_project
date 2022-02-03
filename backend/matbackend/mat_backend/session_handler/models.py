from django.db import models
from django.db.models.fields import FloatField
from django.utils import tree
from account.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import int_list_validator

#  Specify a translation string by using the function gettext().
#  It’s convention to import this as a shorter alias, _, to save typing.
from django.utils.translation import gettext_lazy as _

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, null=True)
    founder = models.CharField(max_length=20)
    min_num_of_participants = models.IntegerField()
    max_num_of_participants = models.IntegerField()
    actual_num_of_participants = models.IntegerField()
    tags = ArrayField(models.CharField(max_length=30), blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    creation_date = models.DateField(auto_now_add=True)
    with_test_set = models.BooleanField(default=False)
    test_dataset = models.BinaryField(null=True)
    # model specific parameters
    parameters_keys = ArrayField(models.CharField(max_length=30), null=True)
    parameters_values = ArrayField(models.CharField(max_length=30), null=True)
    model_name = models.CharField(max_length=200, null=True)
    private_key = models.CharField(max_length=1000, null = True)
    federated_round = models.IntegerField(default = 1, null = False)
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
    related_session = models.ForeignKey(Session, on_delete = models.CASCADE)

class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    session = models.ForeignKey(Session, on_delete = models.SET_NULL, null=True)
    # model = models.ForeignKey(MLModel, on_delete = models.SET_NULL, null=True)
    local_data_count = models.IntegerField(null=True)
    weights_uploaded = models.ForeignKey(StorageFile, on_delete = models.SET_NULL, null=True)
    accuracy = models.FloatField(null=True)
    loss = models.FloatField(null=True)
    # are local weights uploaded
    is_model_uploaded = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    @property
    def user_name(self):
        return self.user.username


class SessionResult(models.Model):
    session_result_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(Session, on_delete = models.SET_NULL, null=True)
    finished = models.BooleanField(default=False)
    global_model_accuracy = models.FloatField(null=True)
    global_model_loss = models.FloatField(null=True)
    federated_round = models.IntegerField(default=1, null=False)
    # global_model = models.ForeignKey(MLModel, on_delete=models.CASCADE)
