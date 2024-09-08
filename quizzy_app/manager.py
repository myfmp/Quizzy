from .models import *
from django.db.models import IntegerField
from django.db.models.functions import Cast

def change_quizz_title(title, quizz_id):
    new_title = Quizz.objects.get(id=quizz_id)
    new_title.Title = title
    new_title.save()

def restrict_quizz(password, quizz_id):
    quizz = Quizz.objects.get(id=int(quizz_id))
    quizz.Settings = ['ACCESS',str(password)]
    quizz.save()

def unlock_quizz(quizz_id):
    quizz = Quizz.objects.get(id=int(quizz_id))
    quizz.Settings = ['EMPTY']
    quizz.save()

def change_question_content(content, question_id):
    new_content = Question.objects.get(id=question_id)
    new_content.Content = content
    new_content.save()

def delete_quizz(quizz_id):
   quizz = Quizz.objects.get(id=int(quizz_id))
   quizz.delete()
   try:
       questions = Question.objects.filter(Quizz_id=quizz_id) 
       questions.delete()
   except:
       print('null')
   try:
       choices = Choice.objects.filter(Quizz_id=quizz_id)
       choices.delete()
   except:
       print('null')

def reset_quizz(quizz_id):
   try:
       questions = Question.objects.filter(Quizz_id=quizz_id) 
       questions.delete()
   except:
       print('null')
   try:
       choices = Choice.objects.filter(Quizz_id=quizz_id)
       choices.delete()
   except:
       print('null')
     
def change_question_order(question_order):
    for querry_data in question_order:
        new_order = Question.objects.get(id=querry_data[1])
        new_order.Order = querry_data[0]
        new_order.save()

def add_question(content, quizz_id):
    Questions = Question.objects.filter(Quizz_id=quizz_id).annotate(order_as_int=Cast('Order', IntegerField())).order_by('order_as_int')
    if Questions.exists():
        Last_Order = Questions.last().Order
        Assign_Order = str(int(Last_Order) + 1)
    else:
        Assign_Order = '1'
    new_question = Question(
        Quizz_id=quizz_id,
        Content=content,
        Scoring='1',
        Order = Assign_Order
    )
    new_question.save() 
    new_question_data = [str(new_question.id),new_question.Order,new_question.Content]
    return new_question_data

def add_choice(choice, question_id, quizz_id):
    Choice_Data = []
    try:
        Choice_To_Add = Choice(
            Quizz_id = str(quizz_id),
            Question_id = str(question_id),
            Content = choice,
            Correction = False
        )
        Choice_To_Add.save()
        Choice_Data = [str(Choice_To_Add.id), Choice_To_Add.Content, Choice_To_Add.Correction, Choice_To_Add.Question_id]
        return Choice_Data
    except:
        return Choice_Data
    
def change_choice_truth_value(choice_id, choice_truth_value):
    choice = Choice.objects.get(id=choice_id)
    if choice_truth_value == 'true':
     choice.Correction = True
    else:
     choice.Correction = False
    choice.save()

def change_choice_content(choice_id, choice_content):
   new_content = Choice.objects.get(id=choice_id)
   new_content.Content = choice_content
   new_content.save()   

def delete_choice(choice_id):
   choice = Choice.objects.get(id=choice_id)
   choice.delete()

def delete_question(question_id):
   question = Question.objects.get(id=int(question_id)) 
   choices = Choice.objects.filter(Question_id=question.id)
   choices.delete()
   question.delete()   
