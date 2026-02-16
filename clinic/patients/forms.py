from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone', 'age', 'gender', 'location']
        widgets = {
            'gender': forms.Select(choices=Patient.GENDER_CHOICES),
        }
