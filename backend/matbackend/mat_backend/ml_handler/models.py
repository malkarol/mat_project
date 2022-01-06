from django.db import models

#  Specify a translation string by using the function gettext().
#  It’s convention to import this as a shorter alias, _, to save typing.
from django.utils.translation import gettext_lazy as _

class MLModel(models.Model):
    ml_model_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    creation_date = models.DateField(auto_now_add=True)
    model_parameters_json = models.CharField(max_length=1000, null=True)
    class ModelTypesEnum(models.IntegerChoices):
        IMAGECLASS = 0, _('ImageClassification')
        TEXTCLASS= 1, _('TextClassification')

    model_type = models.IntegerField(
      choices=ModelTypesEnum.choices,
      default=ModelTypesEnum.IMAGECLASS
    )
