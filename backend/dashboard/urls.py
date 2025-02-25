from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

app_name = "dashboard"

urlpatterns = [
    path("", home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", authView, name="authView"),
    path("logout/", custom_logout, name="logout"),
    path("exams/", getExam, name="getExam"),
    path("students/", getStudent, name="getStudent"),
    path("students/login/", LoginView.as_view(), name="loginStudent"),
    path("students/signup/", RegisterStudentView.as_view(), name="registerStudent"),
    path('students/update_marks/', UpdateMarksView.as_view(), name='update_marks'),
    path("students/upload_video/", upload_video, name="upload_video"),
    path("students/audio_report/<int:id>", audio_report, name="audio_report"),
    path("students/generate-report/<int:id>", generate_report, name="generate_report"),
    path("students/remove_activity/<int:id>", remove_suspicious_activity, name="remove_activity"),
]

