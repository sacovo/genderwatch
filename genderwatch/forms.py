"""
forms
"""
from django import forms
from django.forms import ModelForm
from genderwatch.models import Verdict, Event

class VerdictForm(ModelForm):
    """
    Form for providing infos about a verdict.
    """
    gender = forms.ChoiceField(choices=Verdict.GENDERS)
    position = forms.ChoiceField(choices=Verdict.POSITIONS)
    category = forms.ChoiceField(choices=Verdict.CATEGORIES)

    class Meta:
        model = Verdict
        fields = ['gender', 'position', 'category']

class EventForm(ModelForm):
    """
    Form for creating an event
    """
    class Meta:
        model = Event
        fields = ['gender', 'position', 'category']
