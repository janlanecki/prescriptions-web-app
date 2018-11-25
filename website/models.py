from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


class Patient(User):
    """Let's assume a username is a pesel number."""
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    pesel = models.PositiveIntegerField(primary_key=True)
    date_of_birth = models.DateField()
    conditions = models.ManyToManyField('Condition', blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Patient'


class Doctor(User):
    """Let's assume a username is a doctor's number needed for receipt."""
    TITLES = (
        ('LE', 'lek.'),
        ('DR', 'dr n. med.'),
        ('DH', 'dr hab. n. med.'),
        ('PR', 'prof. dr hab. n. med.'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    title = models.CharField(max_length=2, choices=TITLES, default=TITLES[0][0])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    patients = models.ManyToManyField('Patient', blank=True)

    def __str__(self):
        return self.get_title_display() + ' ' + self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Doctor'


class Condition(models.Model):
    """A condition of a patient making him eligible for a refund."""
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Condition'


class StoryEntry(models.Model):
    """Single entry in a patient's story. Holds information either only about a disease
       or about a disease and a prescription."""
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    disease = models.ForeignKey('Disease', blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(max_length=500, null=True)

    def __str__(self):
        if self.disease is None:
            return self.doctor.last_name + ' -> ' + self.patient.last_name + ' "' + self.description + '"'
        return self.doctor.last_name + ' -> ' + self.patient.last_name + ' "' + self.disease.name + '"'

    class Meta:
        verbose_name = 'StoryEntry'
        verbose_name_plural = 'StoryEntries'


class Disease(models.Model):
    """Disease coded with ICD 10"""
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'Disease'


class Prescription(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doctor.last_name + ' -> ' + self.patient.last_name + ' ' + str(self.date.day) + '-' + str(self.date.month) + '-' + str(self.date.year)

    class Meta:
        verbose_name = 'Prescription'


class PrescriptionEntry(models.Model):
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE)
    medication = models.ForeignKey('Medication', on_delete=models.CASCADE)
    dosage = models.ForeignKey('Dosage', null=True, on_delete=models.SET_NULL)
<<<<<<< Updated upstream
    refund = models.ForeignKey('Refund', null=True, on_delete=models.SET_NULL)
=======
    refund = models.ForeignKey('Refund', on_delete=models.CASCADE, null=True, blank=True)
>>>>>>> Stashed changes

    def __str__(self):
        return self.medication.name

    class Meta:
        verbose_name = 'PrescriptionEntry'
        verbose_name_plural = 'PrescriptionEntries'


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
            dosage += '1 raz dziennie'
        else:
            dosage += str(self.doses_per_day) + ' razy dziennie'
        if self.days_between_doses != 0:
            dosage += ' co ' + str(self.days_between_doses) + ' dni'
        return dosage + ' ' + self.get_time_of_day_display() + ' ' + self.get_eating_relation_display()

    class Meta:
        verbose_name = 'Dosage'


class Medication(models.Model):
    FORM = (
        ('TB', 'tabletki'),
        ('ZS', 'zastrzyki'),
        ('KR', 'krople'),
        ('KP', 'kapsulki'),
        ('AM', 'ampulki'),
        ('FL', 'fiolki'),
    )
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    active_substance = models.ManyToManyField('Substance')
    form = models.CharField(max_length=2, choices=FORM)
    amount = models.PositiveIntegerField()
    mg_of_active_substance = models.PositiveIntegerField()

    def __str__(self):
        return self.name + " " + str(self.amount) + self.get_form_display() + ' ' + str(self.mg_of_active_substance) + 'mg'

    class Meta:
        verbose_name = 'Medication'


class Substance(models.Model):
    """Active substance checked when checking interactions"""
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Substance'


class Refund(models.Model):
    medication = models.ForeignKey('Medication', on_delete=models.CASCADE)
    condition = models.ForeignKey('Condition', blank=True, null=True, on_delete=models.CASCADE)
    percentage = models.FloatField() # 0% if full refund

    def __str__(self):
        return self.medication.name + ' on ' + str(self.percentage) + '%'

    class Meta:
        verbose_name = 'Refund'


class Interaction(models.Model):
    substance1 = models.ForeignKey('Substance', related_name='first', on_delete=models.CASCADE)
    substance2 = models.ForeignKey('Substance', related_name='second', on_delete=models.CASCADE)
    severity = models.IntegerField() # 1 to 5, 5 being most severe

    def __str__(self):
        return self.substance1.name + ' + ' + self.substance2.name + ' = ' + str(self.severity)

    class Meta:
        verbose_name = 'Interaction'
