from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import IntegerField
from django.db.models.functions import Cast
from .models import *
import ast
import json
from .encryptor import  *
from .manager import *
from .corrector import *
from .uploader import *
from .latex import *
from .scorer import *

# Create your views here.
@login_required
def dashboard(request):
   if request.method == 'POST':
      New_Quizz_Title = request.POST.get('New_Quizz_Title')
      new_quizz = Quizz(
         Owner_id=request.user.id,
         Title=New_Quizz_Title,
         Settings=['EMPTY']
      )
      new_quizz.save() 
      default_question = Question(
          Quizz_id=str(new_quizz.id),
          Content='Enter your first question ...',
          Scoring='1',
          Order = '1'
      )
      default_question.save() 
      Quizz_id = encrypt_data(str(new_quizz.id))
      return JsonResponse({'URL': str(Quizz_id)}) 
   return render(request, "quizzy/dashboard.html")

def editor(request):
   Encrypted_Quizz_id = request.GET.get('session')
   try:
    Actual_Quizz_id = decrypt_data(ast.literal_eval(Encrypted_Quizz_id))
   except:
    return redirect('/')
   if Quizz.objects.filter(id = Actual_Quizz_id).exists():
     Quizz_Data = Quizz.objects.get(id = Actual_Quizz_id)
     Quizz_Title = Quizz_Data.Title
     Quizz_Access = Quizz_Data.Settings
     if Quizz_Access[0] == 'EMPTY':
       quizz_access = False
     else:
       quizz_access = True
       
     #loading the questions
     Get_Quizz_Questions = Question.objects.filter(Quizz_id=Actual_Quizz_id).annotate(order_as_int=Cast('Order', IntegerField())).order_by('order_as_int')
     Quizz_Questions = []
     for User_Quizz_Questions in Get_Quizz_Questions:
       Quizz_Questions.append([User_Quizz_Questions.id, User_Quizz_Questions.Order, User_Quizz_Questions.Content])
    #End loading quetions
     
     #loading the choices
     Get_Questions_Choices = Choice.objects.filter(Quizz_id=Actual_Quizz_id)
     Questions_Choices = []
     for User_Questions_Choices in Get_Questions_Choices:
       Questions_Choices.append([User_Questions_Choices.id,User_Questions_Choices.Question_id,User_Questions_Choices.Content,User_Questions_Choices.Correction])
     #End loading choices

   else:
      return redirect('/')
   if request.method == 'POST' and Quizz.objects.filter(id = Actual_Quizz_id).exists():
     
     Updated_Quizz_Title = request.POST.get('Update_Quizz_Title')
     Updated_Question_Content = request.POST.get('Update_Question_Content')
     Question_to_Update_Id = request.POST.get('Question_to_update_Id')
     Question_Order =  request.POST.get('New_Questions_Order')
     New_Question =  request.POST.get('New_Question_Content')
     New_Choice =  request.POST.get('New_Choice')
     New_Choice_Question_Id =  request.POST.get('Question_Id')
     To_Update_Choice_Truth_Value = request.POST.get('Truth_Value')
     To_Update_Choice_Id = request.POST.get('Choice_to_update_id')
     Choice_to_update_Id = request.POST.get('Choice_to_update_Id')
     Updated_Choice_Content = request.POST.get('Updated_Choice_Content')
     Choice_To_Delete_id = request.POST.get('Choice_To_Delete_id')
     Question_To_Delete_Id = request.POST.get('Question_To_Delete_Id')
     Auto_Correct = request.POST.get('Auto_Correct')
     file = request.FILES.get('file')
     Delete_Quizz = request.POST.get('Delete_Quizz')
     Reset_Quizz = request.POST.get('Reset_Quizz')
     Quizz_Password = request.POST.get('Quizz_Password')
     Quizz_unlocked = request.POST.get('Quizz_Unlocked')
     Math_Expressions = request.POST.get('IsMath')

     if Math_Expressions:
       MathExpressions(Actual_Quizz_id)
       return JsonResponse({'DATA': 'null'})

     if Quizz_unlocked:
       unlock_quizz(Actual_Quizz_id)
       return JsonResponse({'DATA': 'null'})

     if Quizz_Password:
       restrict_quizz(encrypt_data(Quizz_Password),Actual_Quizz_id)
       return JsonResponse({'DATA': 'null'})
     if Reset_Quizz:
       reset_quizz(str(Actual_Quizz_id))
       return JsonResponse({'DATA': 'null'})

     if Delete_Quizz:
      delete_quizz(str(Actual_Quizz_id))
      return JsonResponse({'DATA': 'null'})

     if file:
      upload_file(file, Actual_Quizz_id)

     if Auto_Correct:
       auto_correct(Actual_Quizz_id)
       return JsonResponse({'DATA': 'null'})

     if Question_To_Delete_Id:
       delete_question(Question_To_Delete_Id)

     if Choice_To_Delete_id:
       delete_choice(Choice_To_Delete_id)

     if Choice_to_update_Id and Updated_Choice_Content:
       change_choice_content(Choice_to_update_Id, Updated_Choice_Content)

     if To_Update_Choice_Id and To_Update_Choice_Truth_Value:
       change_choice_truth_value(To_Update_Choice_Id,To_Update_Choice_Truth_Value)

     if New_Choice and New_Choice_Question_Id:
       New_Choice_Data = add_choice(New_Choice, New_Choice_Question_Id, Actual_Quizz_id)
       return JsonResponse({'DATA': New_Choice_Data})

     if New_Question:
       New_Question_Data = add_question(New_Question, Actual_Quizz_id)
       return JsonResponse({'DATA': New_Question_Data}) 

     if Question_Order:
       Question_Order_Array = json.loads(Question_Order)
       change_question_order(Question_Order_Array)

     if Updated_Question_Content and Question_to_Update_Id:
       change_question_content(Updated_Question_Content, Question_to_Update_Id)

     if Updated_Quizz_Title:
       change_quizz_title(Updated_Quizz_Title ,Actual_Quizz_id)

   return render(request, "quizzy/editor.html" , {'Quizz_id': str(encrypt_data_2(str(Actual_Quizz_id))),'Quizz_Title': Quizz_Title, 'Quizz_Questions': Quizz_Questions, 'Questions_Choices': Questions_Choices, 'Quizz_Access': quizz_access})

def quiz(request):
   Encrypted_Quizz_id = request.GET.get('session')
   Quizz_Password = request.GET.get('password')
   try:
    Actual_Quizz_id = decrypt_data_2(ast.literal_eval(Encrypted_Quizz_id))
   except:
    return redirect('/')
   if Quizz.objects.filter(id = Actual_Quizz_id).exists():
     Quizz_Data = Quizz.objects.get(id = Actual_Quizz_id)
     Quizz_Title = Quizz_Data.Title
     Quizz_Access = Quizz_Data.Settings
     if Quizz_Access[0] == 'EMPTY':
          quizz_access = True
     else:
          Fetch_Quizz = Quizz.objects.filter(id=Actual_Quizz_id)
          if Quizz_Password and Fetch_Quizz.exists():
              Fetch_Quizz_Key = Quizz.objects.get(id=Actual_Quizz_id)
              if str(decrypt_data(ast.literal_eval(Fetch_Quizz_Key.Settings[1]))) == Quizz_Password:
                quizz_access = True
              else:
                quizz_access = False
          else:
              quizz_access = False

     #loading the questions
     Get_Quizz_Questions = Question.objects.filter(Quizz_id=Actual_Quizz_id).annotate(order_as_int=Cast('Order', IntegerField())).order_by('order_as_int')
     Quizz_Questions = []
     for User_Quizz_Questions in Get_Quizz_Questions:
       Quizz_Questions.append([User_Quizz_Questions.id, User_Quizz_Questions.Order, User_Quizz_Questions.Content])
    #End loading quetions
     
     #loading the choices
     Get_Questions_Choices = Choice.objects.filter(Quizz_id=Actual_Quizz_id)
     Questions_Choices = []
     for User_Questions_Choices in Get_Questions_Choices:
       Questions_Choices.append([User_Questions_Choices.id,User_Questions_Choices.Question_id,User_Questions_Choices.Content,User_Questions_Choices.Correction])
     #End loading choices

     if request.method == 'POST':
       User_Answers = request.POST.get('User_Answers')
       
       if User_Answers:
        # x/Question_Count
        Question_Count = Question.objects.filter(Quizz_id=Actual_Quizz_id).count()

        User_Answers_Py = json.loads(User_Answers)

        results, score_counter = score(Actual_Quizz_id, User_Answers_Py)

        Average = score_counter/Question_Count if Question_Count > 0 else 0

        if Average > 0.5:
          Apreciation = "PASS"
        else:
          Apreciation = "FAIL"

        # Prepare the JSON response with both results and score
        return JsonResponse({'DATA': results, 'SCORE': score_counter,'SCORING':Question_Count,'APRECIATION':Apreciation})

   else:
      return redirect('/')
   return render(request,"quizzy/quiz.html", {'Quiz_id':Encrypted_Quizz_id,'Quizz_Title': Quizz_Title ,'Quizz_Questions': Quizz_Questions, 'Questions_Choices':Questions_Choices, 'Quizz_Access': quizz_access})