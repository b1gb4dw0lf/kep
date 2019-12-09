from django.forms import Form
from django import forms


class CostForm(Form):
    error_css_class = 'uk-form-danger'
    min_budget = forms.DecimalField(label='Min Budget', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter minimum budget range'
    }))
    max_budget = forms.DecimalField(label='Max Budget', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter maximum budget range'
    }))
    min_temperature = forms.DecimalField(label='Max Budget', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter minimum temperature'
    }))
    max_temperature = forms.DecimalField(label='Max Budget', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter maximum temperature'
    }))
    postcode = forms.DecimalField(label='Max Budget', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter your postcode'
    }))
    price_per_watt = forms.DecimalField(label='Price/Watt', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter desired price per watt'
    }))
    land_area = forms.DecimalField(label='Land Area', required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter area of the land'
    }))
    materials = forms.ChoiceField(choices=[(1, 'Material 1'), (2, 'Material 2'), (3, 'Material 3')],
                                  widget=forms.Select(attrs={'class': 'uk-select'}), required=False)
    electricity = forms.DecimalField(required=False, widget=forms.TextInput(attrs={
        'class': 'uk-input',
        'placeholder': 'Enter your electricity need'
    }))
    '''
    slider = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'type': 'range', 'step': '1', 'min': '1', 'max': '148', 'class': 'uk-range'}),
        required=False)
    '''
