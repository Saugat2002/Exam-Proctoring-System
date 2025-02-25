from django.urls import path, include
from .views import *


urlpatterns = [
    # path("quiz/", home),
    # path("quiz/quiz/", quiz),
    path("get_quiz/",get_quiz),
]
