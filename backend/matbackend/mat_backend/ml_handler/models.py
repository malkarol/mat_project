from django.db import models
from account.models import User
#  Specify a translation string by using the function gettext().
#  It’s convention to import this as a shorter alias, _, to save typing.
from django.utils.translation import gettext_lazy as _

class MLModel(models.Model):
    ml_model_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    creation_date = models.DateField()
    model_parameters_json = models.CharField(max_length=1000)

    class ModelTypesEnum(models.IntegerChoices):
        IMAGECLASS = 0, _('ImageClassification')
        TEXTCLASS= 1, _('TextClassification')

    model_type = models.IntegerField(
      choices=ModelTypesEnum.choices,
      default=ModelTypesEnum.IMAGECLASS
    )
