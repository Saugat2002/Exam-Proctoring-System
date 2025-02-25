from django.db import models
import uuid

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta: # abstract = True means this model will not be created in database
        abstract = True
    
class Exam(BaseModel):
    exam_name = models.CharField(max_length=100)
    total_marks = models.IntegerField()
    passing_marks = models.IntegerField()
    duration = models.IntegerField()

    def __str__(self):
        return self.exam_name

class Student(BaseModel):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    exam_given = models.CharField(max_length=100, blank=True, null=True, default="Fuse Entrance")
    suspicoius_activity = models.BooleanField(default=False)
    marks_obtained = models.IntegerField(default=0)
    video_report = models.URLField(max_length=500, blank=True, null=True)
    audio_report = models.URLField(max_length=500, blank=True, null=True)
    recording = models.FileField(upload_to='proctoring_videos/', blank=True, null=True)

    def __str__(self):
        return self.username
