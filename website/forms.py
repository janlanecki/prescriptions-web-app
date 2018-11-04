from django.forms import ModelForm
from django import forms
from .models import *

class DosageForm(ModelForm):

	class Meta:
		model = Dosage 
		fields = '__all__'

class PrescriptionForm(ModelForm):
	class Meta:
		model = PrescriptionEntry
		fields = ['prescription', 'medication']