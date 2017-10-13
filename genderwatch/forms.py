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
    gender = forms.ChoiceField(choices=Verdict.GENDERS, widget=forms.RadioSelect)
    position = forms.ChoiceField(choices=Verdict.POSITIONS, widget=forms.RadioSelect)
    category = forms.ChoiceField(choices=Verdict.CATEGORIES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        assembly = kwargs.get('assembly', None)
        del kwargs['assembly']
        super(VerdictForm, self).__init__(*args, **kwargs)
        positions = assembly.positions.split(',')
        choices = [(p[0],p[1]) for p in Verdict.POSITIONS if p[0] in positions]
        self.fields['position'].choices = choices

    class Meta:
        model = Verdict
        fields = ['gender', 'position', 'category']

class EventForm(ModelForm):
    """
    Form for creating an event
    """
    def __init__(self, *args, **kwargs):
        button_text = kwargs.get('button_text', '')
        if button_text:
            del kwargs['button_text']
        super(EventForm, self).__init__(*args, **kwargs)
        self.button_text = button_text
        
    class Meta:
        model = Event
        fields = ['gender', 'position', 'category']
        widgets = {
            'gender': forms.HiddenInput(),
            'position': forms.HiddenInput(),
            'category': forms.HiddenInput(),
        }
