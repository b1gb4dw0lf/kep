from django.forms import Form
from django import forms


class CostForm(Form):
    min_budget = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter minimum budget range'
    }))
    max_budget = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter maximum budget range'
    }))
    materials = forms.ChoiceField(choices=[(1, 'Material 1'), (2, 'Material 2'), (3, 'Material 3')],
                                  widget=forms.Select(attrs={'class': 'uk-select'}))
    electricity = forms.DecimalField(widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter your electricity need'
    }))

