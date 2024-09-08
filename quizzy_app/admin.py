from django.contrib import admin
from .models import Quizz, Question, Choice, Attachment 
# Register your models here.

admin.site.register(Quizz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Attachment)