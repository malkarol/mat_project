# Generated by Django 4.0 on 2022-01-06 19:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session_handler', '0005_participant_accuracy'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), null=True, size=None),
        ),
    ]