from django.http import request
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.models import Permission, User
from website.forms import PrescriptionForm, DosageForm
from website.models import Doctor, Patient


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
        doctor_id = request.user.id
        patients = Doctor.objects.get(id=doctor_id).patients.all()
        return render(request, self.template_name, {'patients': patients})


class CreatePrescriptionView(TemplateView):
    template_name='prescription.html'

    def get(self, request, patient_id):
        patient = Patient.objects.get(id=patient_id)
        return render(request, self.template_name, {
            'patient_name': patient.get_full_name,
            'gender': patient.gender,
            'pesel': patient.pesel,
            'date_of_birth': patient.date_of_birth

        })

