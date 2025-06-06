# Generated by Django 5.1.1 on 2024-10-04 05:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('exam_name', models.CharField(max_length=100)),
                ('total_marks', models.IntegerField()),
                ('passing_marks', models.IntegerField()),
                ('duration', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('exam_given', models.CharField(blank=True, default='Test Entrance', max_length=100, null=True)),
                ('suspicoius_activity', models.BooleanField(default=False)),
                ('marks_obtained', models.IntegerField(default=0)),
                ('video_report', models.URLField(blank=True, max_length=500, null=True)),
                ('audio_report', models.URLField(blank=True, max_length=500, null=True)),
                ('recording', models.FileField(blank=True, null=True, upload_to='proctoring_videos/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
