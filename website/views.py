import json

from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import request
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.models import Permission, User
from website.forms import PrescriptionForm, DosageForm
from website.models import Doctor, Patient, Medication, Dosage, Refund, PrescriptionEntry


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


def post(request, patient_id):
    if request.method == 'POST':
        data = request.POST

        #Work in progress

        print("*********")
        print(data)
        names = []
        dosages = []
        refunds = []
        patient = Patient.objects.get(id=patient_id)
        patients_conditions = patient.conditions.all()

        i = 1
        while 'name'+str(i) in data:
            names.append(data['name'+str(i)])
            dosages.append(data['dosage'+str(i)])
            refunds.append(data['refund'+str(i)])
            i += 1

        print(names)
        print(dosages)
        print(refunds)

        medications = []
        dosages = []
        refunds = []

        for n in names:
            None

        for n, d, r in names, dosages, refunds:
            medication = Medication.objects.get(name=n)
            dosage = Dosage.objects.get(pk=d)
            refund = Refund.objects.filter(pk=r)



        if request.POST['name1'] and request.POST['dosage1'] and request.POST['refund1']:
            print(request.POST.get('name1'))
            medication = Medication.objects.get(name=request.POST['name1'])
            post = PrescriptionEntry()
            post.medication = request.POST.get('name1')
            post.dosage = request.POST.get('dosage1')
            post.refund = request.POST.get('refund1')
            post.save()
            print("out create post")
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
    else:
            return HttpResponseForbidden()



