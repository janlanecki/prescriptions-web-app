from django.http import request
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.models import Permission, User
from website.forms import PrescriptionForm, DosageForm
from website.models import Doctor


class FormsView(TemplateView):
    template_name = 'form.html'

    def get(self, request):
        prescription_form = PrescriptionForm()
        dosage_form = DosageForm()
        return render(request, self.template_name, {'prescription_form': prescription_form, 'dosage_form': dosage_form})

    def post(self, request):
        prescription_form = PrescriptionForm(request.POST)
        dosage_form = DosageForm(request.POST)

        if prescription_form.is_valid() and dosage_form.is_valid():
            dosage_item = dosage_form.save()
            prescription_item = prescription_form.save(commit=False)
            prescription_item.dosage = dosage_item
            prescription_item.save()

        return render(request, self.template_name, {'prescription_form': prescription_form, 'dosage_form': dosage_form})


class SelectPatientsView(TemplateView):
    template_name = "select_patient.html"

    def get(self, request):
        doctor = request.user.id
        patients = Doctor(pk=doctor).patients.all()
        print(patients)
        return render(request, self.template_name, {'patients': patients})
