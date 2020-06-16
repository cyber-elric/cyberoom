# coding=utf-8

from django.urls import path
from . import views


app_name = 'pensieve'
urlpatterns = [
    path('', views.PensieveList.as_view(), name='list'),
    path('<int:pk>/', views.PensieveDetail.as_view(), name='detail'),
    path('update/<int:pk>/', views.PensieveUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', views.PensieveDelete.as_view(), name='delete'),
    path('new/', views.PensieveCreate.as_view(), name='create'),
]
