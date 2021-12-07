# Generated by Django 3.2.9 on 2021-12-07 17:43

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('Fullname', models.CharField(max_length=30)),
                ('PricingPlan', models.IntegerField(choices=[(1, 'Registered'), (2, 'Premium')], default=1)),
                ('UserType', models.IntegerField(choices=[(0, 'Admin'), (1, 'Normal')], default=0)),
                ('MLBackground', models.IntegerField(blank=True, choices=[(0, 'Student'), (1, 'Professor'), (2, 'Professional')], default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MLModel',
            fields=[
                ('MLModelID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=150)),
                ('CreationDate', models.DateField()),
                ('ModelParametersJSON', models.CharField(max_length=1000)),
                ('ModelType', models.IntegerField(choices=[(0, 'ImageClassification'), (1, 'TextClassification')])),
                ('Owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('ParticipantID', models.AutoField(primary_key=True, serialize=False)),
                ('ModelUploaded', models.BooleanField()),
                ('IsOwner', models.BooleanField()),
                ('LocalPath', models.CharField(max_length=400)),
                ('GlobalPath', models.CharField(max_length=400)),
                ('Model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mat_backend.mlmodel')),
            ],
        ),
        migrations.CreateModel(
            name='SessionResult',
            fields=[
                ('SessionResultID', models.AutoField(primary_key=True, serialize=False)),
                ('LocalModelsAccuracyJSON', models.CharField(max_length=1000, null=True)),
                ('Finished', models.BooleanField(default=False)),
                ('GlobalModel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mat_backend.mlmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('SessionID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=200, null=True)),
                ('Description', models.CharField(max_length=400, null=True)),
                ('PricingPlan', models.IntegerField(choices=[(1, 'Registered'), (2, 'Premium')])),
                ('MinNumOfParticipants', models.IntegerField()),
                ('MaxNumOfParticipants', models.IntegerField()),
                ('ActualNumOfParticipants', models.IntegerField()),
                ('StartDate', models.DateField()),
                ('EndDate', models.DateField(null=True)),
                ('CreationDate', models.DateField()),
                ('WithTestSet', models.BooleanField(default=False)),
                ('TestDataset', models.BinaryField(null=True)),
                ('Founder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mat_backend.participant')),
                ('Result', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mat_backend.sessionresult')),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='Session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mat_backend.session'),
        ),
        migrations.AddField(
            model_name='participant',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
