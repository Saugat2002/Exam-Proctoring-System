from django.db import models
from django.utils import timezone
from dashboard.models import Student

# class ExamSession(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     start_time = models.DateTimeField(auto_now_add=True)
#     end_time = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"Exam session for {self.student} at {self.start_time}"

class SuspiciousActivity(models.Model):
    # exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    activity_type = models.CharField(max_length=255)
    screenshot = models.ImageField(upload_to='static/suspicious_activities/')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.activity_type} at {self.timestamp}"
