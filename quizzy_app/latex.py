from .models import *
from django.db.models import IntegerField
from django.db.models.functions import Cast

def MathExpressions(quizz_id):
    Exam = []

    # Collecting questions and choices
    Questions = Question.objects.filter(Quizz_id=quizz_id).annotate(order_as_int=Cast('Order', IntegerField())).order_by('order_as_int')
    for question in Questions:
        tmp = [[question.id, question.Content]]
        Choices = Choice.objects.filter(Question_id=question.id)
        for choice in Choices:
            tmp.append([choice.id, choice.Content])
        Exam.append(tmp)

    return Exam