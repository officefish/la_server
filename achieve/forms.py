__author__ = 'RIK'
from django import forms
from hero.models import Hero

ACHIEVE_TYPE_CHOISES = [
    ('0', 'магия'),
    ('1', 'магия по цели')
]

RARITY_CHOICES = [
    ('0', 'обычная'),
    ('1', 'редкая'),
    ('2', 'эпическая'),
    ('3', 'легендарная'),
]


class AchieveForm (forms.Form):
    title = forms.CharField(
        max_length=70, widget=forms.TextInput(attrs={'maxlength': 70}))
    description = forms.CharField(
        required=False, max_length=200, widget=forms.Textarea(attrs={'maxlength': 200}))
    price = forms.IntegerField(
        max_value=30, widget=forms.TextInput(attrs={'maxlength': 2}))
    autonomic = forms.TypedChoiceField(coerce=lambda x: bool(int(x)),
                                       choices=((0, 'False'), (1, 'True')),
                                       widget=forms.RadioSelect
                                       )
    type = forms.ChoiceField(
        choices=ACHIEVE_TYPE_CHOISES, widget=forms.RadioSelect())


class AddAchieveOwnerForm (forms.Form):

    def __init__(self, *args, **kwargs):
        super(AddAchieveOwnerForm, self).__init__(*args, **kwargs)

        hero_choises = [(-1, '----')]
        hero_choises += [(o.id, str(o.title)) for o in Hero.objects.all()]

        self.fields['hero'] = forms.ChoiceField(choices=hero_choises)


class AchieveMaskForm (forms.Form):
    rarity = forms.ChoiceField(choices=RARITY_CHOICES)
    buy_cost = forms.IntegerField(
        widget=forms.TextInput(attrs={'maxlength': 4}))
    sale_cost = forms.IntegerField(
        widget=forms.TextInput(attrs={'maxlength': 4}))
    access = forms.IntegerField(widget=forms.TextInput(attrs={'maxlength': 4}))
    max_access = forms.IntegerField(
        widget=forms.TextInput(attrs={'maxlength': 4}))
    craft_available = forms.TypedChoiceField(required=False, coerce=lambda x: bool(int(x)),
                                             choices=((0, 'False'),
                                                      (1, 'True')),
                                             widget=forms.RadioSelect
                                             )
