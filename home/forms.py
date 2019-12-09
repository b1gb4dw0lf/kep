from django.forms import Form
from django import forms
from django_countries.data import COUNTRIES

CHOICES = tuple([(u'', '----------')] + sorted(COUNTRIES.items()))

class HomeUserForm(Form):
    error_css_class = 'uk-form-danger'
    min_budget = forms.DecimalField(label='Min Budget', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter minimum budget range'
    }))
    max_budget = forms.DecimalField(label='Max Budget', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter maximum budget range'
    }))
    postcode = forms.DecimalField(label='Postcode', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter your postcode'
    }))
    country = forms.ChoiceField(choices=CHOICES,
                                widget=forms.Select(attrs={'class': 'uk-select'}))
    electricity = forms.DecimalField(required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter your electricity need'
    }))
    grid_type = forms.ChoiceField(choices=[(0, 'On-Grid'), (1, 'Off-Grid')],
                                  widget=forms.Select(attrs={'class': 'uk-select'}),
                                  required=False)


class CommercialUserForm(Form):
    error_css_class = 'uk-form-danger'
    min_budget = forms.DecimalField(label='Min Budget', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter minimum budget range'
    }))
    max_budget = forms.DecimalField(label='Max Budget', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter maximum budget range'
    }))
    min_temperature = forms.DecimalField(label='Min Temperature', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter minimum temperature'
    }))
    max_temperature = forms.DecimalField(label='Max Temperature', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter maximum temperature'
    }))
    postcode = forms.DecimalField(label='Postcode', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter your postcode'
    }))
    country = forms.ChoiceField(choices=CHOICES,
                                widget=forms.Select(attrs={'class': 'uk-select'}))
    price_per_watt = forms.DecimalField(label='Price/Watt', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter desired price per watt'
    }))
    land_area = forms.DecimalField(label='Land Area', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter area of the land'
    }))
    materials = forms.ChoiceField(choices=[(0, None), (1, 'Material 1'), (2, 'Material 2'), (3, 'Material 3')],
                                  widget=forms.Select(attrs={'class': 'uk-select'}), required=False)
    electricity = forms.DecimalField(required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter your electricity need'
    }))
    grid_type = forms.ChoiceField(choices=[(0, 'On-Grid'), (1, 'Off-Grid')],
                                  widget=forms.Select(attrs={'class': 'uk-select'}),
                                  required=False)
