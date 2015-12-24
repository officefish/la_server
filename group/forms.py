__author__ = 'RIK'
from django import forms


class GroupForm (forms.Form):
    title = forms.CharField(
        max_length=70, widget=forms.TextInput(attrs={'maxlength': 70}))
    description = forms.CharField(
        max_length=200, widget=forms.Textarea(attrs={'maxlength': 200}))
