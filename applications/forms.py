from django import forms
from .models import Application


class DateInput(forms.DateInput):
    input_type = 'date'


class ApplicationForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

    class Meta:
        model = Application
        fields = ('start_date', 'end_date',)
