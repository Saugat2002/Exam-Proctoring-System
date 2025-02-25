from django.urls import path
from .views import *

urlpatterns = [
    path('detect/', detect_mobile, name='detect_mobile'),
]