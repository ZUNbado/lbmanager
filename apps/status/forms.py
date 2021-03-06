from django import forms
from django.forms.extras.widgets import SelectDateWidget
from .widgets import SelectTimeWidget
from datetime import datetime, timedelta

def now():
    return datetime.today()

def past():
    return datetime.today() - timedelta(hours=1)

class GraphForm(forms.Form):
    start_date = forms.DateField(label='Data Inici',widget=SelectDateWidget(),initial=past())
    start_time = forms.TimeField(label='Hora inici',widget=SelectTimeWidget(),initial=past())

    end_date = forms.DateField(label='Data fi',widget=SelectDateWidget(),initial=now())
    end_time = forms.TimeField(label='Hora fi',widget=SelectTimeWidget(),initial=now())
