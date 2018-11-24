from django.urls import path, include
from .views import FormsView
from django.contrib import admin

urlpatterns = [
    path('prescription', FormsView.as_view(), name='forms'),
]
