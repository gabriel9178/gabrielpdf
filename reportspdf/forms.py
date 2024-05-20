from django import forms
from .models import LabReport

class LabReportForm(forms.ModelForm):
    name = forms.CharField(max_length=100)  # Add a field for the name

    class Meta:
        model = LabReport
        fields = ['pdf_file']



class LogoutForm(forms.Form):
    pass        