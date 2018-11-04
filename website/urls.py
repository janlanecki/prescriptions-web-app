from django.conf.urls import url
from .views import FormsView

urlpatterns = [
    url(r'^$', FormsView.as_view(), name='forms'),
]