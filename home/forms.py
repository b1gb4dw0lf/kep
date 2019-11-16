from django.forms import Form
from django import forms


class CostForm(Form):
    min_budget = forms.DecimalField(help_text="Enter minimum budget range")
    max_budget = forms.DecimalField(help_text="Enter maximum budget range")
    materials = forms.ChoiceField(choices=[(1, 'Material 1'), (2, 'Material 2'), (3, 'Material 3')])
    electricity = forms.DecimalField(help_text="Enter your electricity need")

