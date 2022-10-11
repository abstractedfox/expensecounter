
from django.contrib import admin
from django.urls import include, path
from . import views

app_name="ExpenseCounterApp"
urlpatterns = [
    path('', views.index),
    path('setlanguage/<str:setlanguage>', views.set_language, name='set-language'),
    path('index', views.index, name="index"),
    path('deleteitem/<int:dbkey>', views.deleteitem),
    path('test', views.test, name="testy"),
]
