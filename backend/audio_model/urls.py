from django.urls import path
from .views import *

urlpatterns = [
    path('get_audio_report/<int:id>', get_audio_report, name='get_audio_report'),
    # path("view_report/<str:id>", view_report, name="view_report"),
]