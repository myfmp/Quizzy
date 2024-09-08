from django.urls import path
from . import views

urlpatterns = [
    path("dashboard",views.dashboard, name="dashbaord"),
    path("editor",views.editor, name="editor"),
    path("quiz",views.quiz, name="quiz")
]