from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Condition)
admin.site.register(StoryEntry)
admin.site.register(Disease)
admin.site.register(Prescription)
admin.site.register(PrescriptionEntry)
admin.site.register(Dosage)
admin.site.register(Medication)
admin.site.register(Substance)
admin.site.register(Refund)
admin.site.register(Interaction)
#admin.site.register()
