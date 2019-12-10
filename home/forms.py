from django.forms import Form
from django import forms
from django_countries.data import COUNTRIES

CHOICES = tuple([(u'', '----------')] + sorted(COUNTRIES.items()))


class HomeUserForm(Form):
    error_css_class = 'uk-form-danger'
    max_budget = forms.DecimalField(label='Max Budget', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter maximum budget range'
    }))
    max_temperature = forms.DecimalField(label='Max Temperature', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter maximum temperature'
    }))
    shape = forms.ChoiceField(required=False,
                              choices=[('', '----------'), (0, 'Rectangular'), (1, 'Square'), (0, 'Triangle')],
                              widget=forms.Select(attrs={'class': 'uk-select'})
                              )
    postcode = forms.CharField(label='Postcode', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter your postcode'
    }))
    country = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'uk-select'}))
    electricity = forms.DecimalField(required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter your electricity need in kW/h'
    }))
    grid_type = forms.ChoiceField(choices=[(0, 'On-Grid'), (1, 'Off-Grid')],
                                  widget=forms.Select(attrs={'class': 'uk-select'}))


class CommercialUserForm(HomeUserForm):
    error_css_class = 'uk-form-danger'
    price_per_watt = forms.DecimalField(label='Price/Watt', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter desired price per watt'
    }))
    land_area = forms.DecimalField(label='Land Area', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter area of the land'
    }))
    materials = forms.ChoiceField(choices=[('', '----------'), (0, 'Mono-Crystalline'), (1, 'Poly-Crystalline'), (2, 'Thin-Film')],
                                  widget=forms.Select(attrs={'class': 'uk-select'}), required=False)
    grid_type = forms.ChoiceField(choices=[(0, 'On-Grid'), (1, 'Off-Grid')],
                                  widget=forms.Select(attrs={'class': 'uk-select'}),
                                  required=False)
