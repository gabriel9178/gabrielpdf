from django import forms
from .models import LabReport

class LabReportForm(forms.ModelForm):
    name = forms.CharField(max_length=100)  # Add a field for the name
    normal = forms.BooleanField(label='Normal', required=False)  # Checkbox for 'Normal'
    pr = forms.BooleanField(label='PR', required=False)  # Checkbox for 'PR'

    class Meta:
        model = LabReport
        fields = ['name', 'pdf_file', 'normal', 'pr']

class LogoutForm(forms.Form):
    pass       
