# Generated by Django 4.0 on 2022-01-12 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session_handler', '0011_participant_loss'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessionresult',
            name='local_models_accuracy_json',
        ),
        migrations.AddField(
            model_name='sessionresult',
            name='global_model_loss',
            field=models.FloatField(null=True),
        ),
    ]