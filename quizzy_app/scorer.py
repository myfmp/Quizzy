from .models import *
from django.db.models import IntegerField
from django.db.models.functions import Cast

def score(quizz_id):
    # Initialisation questions and choices
    correction = []
    tmp = []

    # Collecting questions and choices
    Questions = Question.objects.filter(Quizz_id=quizz_id).annotate(order_as_int=Cast('Order', IntegerField())).order_by('order_as_int')
    for question in Questions:
        tmp = [str(question.id)]
        Choices = Choice.objects.filter(Question_id=question.id).order_by('id')
        for choice in Choices:
            tmp.append([str(choice.id), choice.Correction])
        correction.append(tmp)

    return correction
