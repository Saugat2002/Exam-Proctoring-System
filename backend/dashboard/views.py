import os
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from visual_model.models import SuspiciousActivity
from .serializers import *
from .models import *

# page after succesful login
@login_required #check if user is logged in or not
def home(request):
    students = Student.objects.all()
    students = list(students.values())
    students = len(students)
    exams = Exam.objects.all()
    exams = list(exams.values())
    exams = len(exams)
    context = {
        'students': students,
        'exams': exams
    }
    return render(request, "main.html", context)

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def custom_logout(request):
    if request.method == "GET":
        # Log out the user
        logout(request)
        # Redirect to main.html
        return redirect("/")
    else:
        # If it's not a GET request, return method not allowed
        return HttpResponseNotAllowed(["GET"])

class RegisterStudentView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        # Check if a student with the given email already exists
        if Student.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Check if user exists
        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            return Response(
                {'message': 'Login failed: User does not exist with entered email.'}
            )
        
        if student.password != password:
            return Response(
                {'message': 'Login failed: Invalid Credentials! Please try again.'}
            )

        # If authentication is successful, return user details
        return Response(
            {
                'message': 'Login successful!',
                'email': student.email,
                'username': student.username,  # Send username to frontend
                'id': student.id,
            },
            status=status.HTTP_200_OK
        )

class UpdateMarksView(APIView):
    def put(self, request):
        email = request.data.get('email')  # Get email from request data
        marks_obtained = request.data.get('marks_obtained')  # Get new marks_obtained value

        if not email or marks_obtained is None:
            return Response({'error': 'Email and marks_obtained are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the student object by email
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the marks_obtained
        student.marks_obtained = marks_obtained
        student.save()

        # Serialize the updated data
        serializer = StudentSerializer(student)

        return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        video = request.FILES.get('video')
        email = request.POST.get('email')  # Assuming the email is sent from the frontend

        if not video or not email:
            return JsonResponse({"status": False, "message": "Invalid data"}, status=400)

        # Fetch the student based on the email
        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            return JsonResponse({"status": False, "message": "Student not found"}, status=404)

        # Check if the student already has a recording and delete the old file if it exists
        if student.recording and default_storage.exists(student.recording.path):
            student.recording.delete(save=False)  # Delete the old recording file

        # Save the new video, overwrite any existing file
        student.recording.save(f"{email}_recording.mp4", video, save=True)

        return JsonResponse({"status": True, "message": "Video uploaded and saved to student record"})

    return JsonResponse({"status": False, "message": "Invalid request method"}, status=405)

def getExam(request):
    exams = Exam.objects.all()
    exams = list(exams.values())
    response = {"exams": exams}
    return render(request, "exams.html", response)

def getStudent(request):
    students = Student.objects.all()
    students = list(students.values())
    response = {"students": students}
    return render(request, "students.html", response)

def audio_report(request, id):
    student = Student.objects.get(id=id)
    email = student.email.replace("@","")
    html_path = rf'reports\audio_reports\{email}_audioreport.html'
    return render(request, f'{html_path}')

import datetime
def generate_report(request, id):

    # Get the student and other necessary data
    student = Student.objects.get(id=id)
    email = student.email.replace("@", "")
    activities = SuspiciousActivity.objects.filter(student=student).order_by('timestamp')
    
    # Group activities by type
    grouped_activities = {}
    for activity in activities:
        if activity.activity_type not in grouped_activities:
            grouped_activities[activity.activity_type] = []
        grouped_activities[activity.activity_type].append(activity)
    
    # Prepare context for the template
    context = {
        'timestamp': datetime.datetime.now(),
        'student': student,
        'grouped_activities': grouped_activities,
    }

    return render(request, 'videoreport_template.html', context)

def remove_suspicious_activity(request, id):
    student = Student.objects.get(id=id)
    SuspiciousActivity.objects.filter(student=student).delete()
    return HttpResponse("Activity removed successfully")