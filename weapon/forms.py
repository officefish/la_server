__author__ = 'RIK'
from django import forms


class WeaponForm (forms.Form):
    title = forms.CharField(
        max_length=70, widget=forms.TextInput(attrs={'maxlength': 70}))
    description = forms.CharField(
        required=False, max_length=200, widget=forms.Textarea(attrs={'maxlength': 200}))
    power = forms.IntegerField(
        max_value=30, widget=forms.TextInput(attrs={'maxlength': 2}))
    strength = forms.IntegerField(
        max_value=30, widget=forms.TextInput(attrs={'maxlength': 2}))
