
from django.contrib import admin
from django.urls import include, path
from . import views

app_name="ExpenseCounterApp"
urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('deleteitem/<int:dbkey>', views.deleteitem),
]
