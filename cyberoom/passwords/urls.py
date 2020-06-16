# coding = utf8

from django.urls import path
from . import views


app_name = 'passwords'
urlpatterns = [
    path('', views.gen_password, name='passwd'),
]
