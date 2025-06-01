from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("dashboard",views.dashboard, name="dashbaord"),
    path("editor",views.editor, name="editor"),
    path("quiz",views.quiz, name="quiz"),
    path("mytree",views.mytree, name="mytree"),
    path("bridge",views.bridge, name="bridge"),
    path("bridge2",views.bridge2, name="bridge2"),
    path("pricing",views.pricing, name="pricing"),
    path("pay",views.pay, name="pay"),
    path("payed",views.payed, name="payed"),
    path("zohoverify/verifyforzoho.html",views.zohoverify, name="zohoverify/verifyforzoho.html")
]
