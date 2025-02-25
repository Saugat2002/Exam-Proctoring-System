from django.db import models
import uuid
import random

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta: # abstract = True means this model will not be created in database
        abstract = True

class Category(BaseModel):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

# create a model for questions such that some question can have multiple correct answers.
class Question(BaseModel):
    question_text = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='category' ,on_delete=models.CASCADE)
    is_multiple_correct = models.BooleanField(default=False)
    marks = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text
    
    def get_answers(self):
        answer_objs = list(Answer.objects.filter(question=self))
        random.shuffle(answer_objs)
        data = []
        for answer_obj in answer_objs:
            data.append({
                'answer': answer_obj.answer_text,
                'is_correct': answer_obj.is_correct
            })
        return data


class Answer(BaseModel):
    answer_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text
