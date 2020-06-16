# coding=utf-8

from django.urls import path
from . import views


app_name = 'gate'
urlpatterns = [
    path('', views.step_in, name='bell'),
    path('check_in/', views.check_in, name='check_in'),
    path('path/', views.the_path, name='path'),
    path('gone/', views.see_you, name='gone'),
]
