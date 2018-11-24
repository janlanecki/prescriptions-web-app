from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class Doctor(User):
    """Let's assume a username is a doctor's number needed for receipt."""
    TITLES = (
        ('LE', 'lek.'),
        ('DR', 'dr n. med.'),
        ('DH', 'dr hab. n. med.'),
        ('PR', 'prof. dr hab. n. med.'),
    )
    gender = models.BooleanField()  # true for Mr./false for Ms.
    title = models.CharField(max_length=2, choices=TITLES, default=TITLES[0][0])

    def __str__(self):
        return self.title + ' ' + self.first_name + ' ' + self.last_name


class Patient(User):
    """Let's assume a username is a pesel number."""
    gender = models.BooleanField() # true for man
    pesel = models.PositiveIntegerField(primary_key=True)
    date_of_birth = models.DateField()
    conditions = models.ManyToManyField('Condition')   


class Condition(models.Model):
    """A condition of a patient making him eligible for a refund."""
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class StoryEntry(models.Model):
    """Single entry in a patient's story. Holds information either only about a disease
       or about a disease and a prescription."""
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', null = True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    #story = models.ForeignKey('Story', on_delete=models.CASCADE) no 'Story' model. Is it necessary?
    disease = models.ForeignKey('Disease', null = True, on_delete=models.SET_NULL)    
    #prescriptions = models.ForeignKey('Prescription', null=True, on_delete=models.SET_NULL)


class Disease(models.Model):
    """Disease coded with ICD 10"""
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=150)

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class Prescription(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    story = models.ForeignKey('StoryEntry', on_delete=models.CASCADE)


class PrescriptionEntry(models.Model):
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE)
    medication = models.ForeignKey('Medication', on_delete=models.CASCADE) 
    dosage = models.ForeignKey('Dosage',null = True, on_delete=models.SET_NULL)


class Dosage(models.Model):
    TIME_OF_DAY = (
        ('NO', ''),
        ('RA', ' rano'),
        ('WI', ' wieczorem'),
    )
    EATING = (
        ('NO', ''),
        ('NC', ' na czczo'),
        ('PJ', ' po jedzeniu'),
    )
    unit = models.CharField(max_length=30)
    doses_per_day = models.SmallIntegerField()
    days_between_doses = models.SmallIntegerField(default=0) # 0 if daily
    time_of_day = models.CharField(max_length=2, choices=TIME_OF_DAY, default=TIME_OF_DAY[0][0])
    eating_relation = models.CharField(max_length=2, choices=EATING, default=EATING[0][0])

    def __str__(self):
        dosage = self.unit + ' '
        if self.doses_per_day == 1:
            dosage += '1 raz'
        else:
            dosage += str(self.doses_per_day) + ' razy'
        if self.days_between_doses == 0:
            dosage += ' dziennie'
        else:
            dosage += 'co ' + str(self.days_between_doses) + ' dni'
        return dosage + self.time_of_day + self.eating_relation


class Medication(models.Model):
    FORM = (
        ('TB', 'tabletki'),
        ('ZS', 'zastrzyki'),
    )
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    active_substance = models.ManyToManyField('Substance')
    form = models.CharField(max_length=2, choices=FORM)
    amount = models.PositiveIntegerField()
    mg_of_active_substance = models.PositiveIntegerField()


class Substance(models.Model):
    """Active substance checked when checking interactions"""
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=150)


#  TODO institutions model