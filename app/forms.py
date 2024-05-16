# forms.py in the officers app
from django import forms
from .models import GatePass

class GatePassForm(forms.ModelForm):
    class Meta:
        model = GatePass
        fields = ['name', 'email', 'dob', 'image', 'contact_no', 'department', 'reason_to_meet']
