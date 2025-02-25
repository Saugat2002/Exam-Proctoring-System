from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import random

# def home(request):
#     context = {"categories" : Category.objects.all()}

#     if request.GET.get('category'):
#         return redirect(f"/quiz/?category={request.GET.get('category')}")
#     return render(request, 'homepage.html', context) 

# def quiz(request):
#     context = {"category" : request.GET.get('category')}
#     return render(request, 'quiz.html', context)

def get_quiz(request):
    try:
        question_objs = Question.objects.all()

        if request.GET.get('category'):
            question_objs = question_objs.filter(category__category_name__icontains=request.GET.get('category'))
        question_objs = list(question_objs)
        data = []
        random.shuffle(question_objs)
        for question_obj in question_objs:
            data.append({
                'uid': question_obj.uid,
                'category': question_obj.category.category_name,
                'question': question_obj.question_text,
                'marks': question_obj.marks,
                'answers': question_obj.get_answers()
            })
        payload = {
                    'status': True,
                   'data': data
                   }
        return JsonResponse(payload)
    
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong")