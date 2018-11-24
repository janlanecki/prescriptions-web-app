from django.urls import path, include
from .views import FormsView
from django.contrib import admin

urlpatterns = [
    path('', FormsView.as_view(), name='forms'),
]
