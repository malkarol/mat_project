# Generated by Django 4.0 on 2021-12-21 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('pricing_plan', models.IntegerField(choices=[(0, 'Free'), (1, 'Paid')], default=0)),
                ('ml_background', models.IntegerField(choices=[(0, 'Student'), (1, 'Professor'), (2, 'Professional'), (3, 'Hobbyst')], default=3)),
                ('user_type', models.IntegerField(choices=[(0, 'Normal'), (1, 'Admin')], default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
