__author__ = 'RIK'
from django import forms

RARITY_CHOICES=[
   ('0','обычная'),
   ('1','редкая'),
   ('2','эпическая'),
   ('3','легендарная'),
   ]


class MaskItemForm (forms.Form):
    rarity = forms.ChoiceField(choices=RARITY_CHOICES)
    buy_cost = forms.IntegerField(widget=forms.TextInput(attrs={'maxlength':4}))
    sale_cost = forms.IntegerField(widget=forms.TextInput(attrs={'maxlength':4}))
    access_simple = forms.IntegerField(widget=forms.TextInput(attrs={'maxlength':4}))
    max_simple = forms.IntegerField(widget=forms.TextInput(attrs={'maxlength':4}))
    access_golden = forms.IntegerField(widget=forms.TextInput(attrs={'maxlength':4}))
    max_golden = forms.IntegerField(widget=forms.TextInput(attrs={'maxlength':4}))
    craft_available = forms.TypedChoiceField(required=False, coerce=lambda x: bool(int(x)),
                   choices=((0, 'False'), (1, 'True')),
                   widget=forms.RadioSelect
                )
