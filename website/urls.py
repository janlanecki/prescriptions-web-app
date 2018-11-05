from django.urls import path
from .views import FormsView

urlpatterns = [
    path('', FormsView.as_view(), name='forms'),
]
