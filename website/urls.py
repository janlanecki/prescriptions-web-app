from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('prescription/patient_id=<patient_id>/api/add_prescription', views.post)
]