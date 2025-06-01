from django.db import models
from django.utils import timezone

class Quizz(models.Model):
    id = models.AutoField(primary_key=True)
    Owner_id = models.CharField(max_length=256)
    Title = models.CharField(max_length=256)
    Settings = models.JSONField()
    Parent_folder_id = models.CharField(max_length=256, default='root')

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    Quizz_id = models.CharField(max_length=256)
    Content = models.CharField(max_length=256, default='none')
    Scoring = models.CharField(max_length=256, default='1')
    Order = models.CharField(max_length=256)

class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    Quizz_id = models.CharField(max_length=256)
    Question_id = models.CharField(max_length=256)
    Content = models.CharField(max_length=256, default='none')
    Correction = models.BooleanField()

class Attachment(models.Model):
    id = models.AutoField(primary_key=True)
    Question_id = models.CharField(max_length=256)
    File_path = models.CharField(max_length=256)

class Folders(models.Model):
    id = models.AutoField(primary_key=True)
    Owner_id = models.CharField(max_length=256)
    Parent_folder_id = models.CharField(max_length=256, default='root')
    Folder_Name = models.CharField(max_length=256)

class Subscriptions(models.Model):
    id = models.AutoField(primary_key=True)
    Owner_id = models.CharField(max_length=256)
    Subscription_type = models.CharField(max_length=256)
    Subscription_id = models.CharField(max_length=256)
    Creation_date = models.DateTimeField(auto_now_add=True)


