from django.db import models
from django.contrib.auth.models import User


class Doctor(User):
    """Let's assume a username is an id number."""
    gender = models.BooleanField()  # Mr./Ms.
    title = models.CharField(max_length=50)  # TODO enum
    id = models.PositiveIntegerField(primary_key=True)


class Patient(User):
    """Let's assume a username is a pesel number."""
    gender = models.BooleanField()
    pesel = models.PositiveIntegerField(max_length=11, primary_key=True)
    date_of_birth = models.DateField()
    conditions = models.ManyToManyField('Condition')

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name'])
        ]


class Condition(models.Model):
    """A condition of a patient making him eligible for a refund."""
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=150)


class StoryEntry(models.Model):
    """Single entry in a patient's story. Holds information either only about a disease
       or about a disease and a prescription."""
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    story = models.ForeignKey('Story', on_delete=models.CASCADE)
    disease = models.ForeignKey('Disease', on_delete=models.SET_NULL)
    prescription = models.ForeignKey('Prescription', null=True, on_delete=models.SET_NULL)


class Disease(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=150)

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]


class Prescription(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    story = models.ForeignKey('StoryEntry', on_delete=models.CASCADE)


class PrescriptionEntry(models.Model):
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE)
    medication = models.ForeignKey('Medication', on_delete=models.SET_NULL)
    size_of_dose = models.PositiveIntegerField()
    unit = models.CharField(max_length=30)  # TODO abbreviation, enum?
    doses_per_day = models.SmallIntegerField()
    days_between_doses = models.SmallIntegerField()  # 0 if daily doses


class Medication(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    active_substance = models.CharField(max_length=150)  # TODO substance model
    form = models.CharField(max_length=150)  # TODO enum
    amount = models.PositiveIntegerField()
    unit = models.CharField(max_length=30)  # TODO unit abbreviation, enum?

#  TODO institutions model
