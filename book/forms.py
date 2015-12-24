__author__ = 'RIK'
from django import forms
from hero.models import Hero


class AddBookOwnerForm (forms.Form):

    def __init__(self, *args, **kwargs):
        super(AddBookOwnerForm, self).__init__(*args, **kwargs)

        hero_choises = [(-1, '----')]
        hero_choises += [(o.id, str(o.title)) for o in Hero.objects.all()]

        self.fields['hero'] = forms.ChoiceField(choices=hero_choises)


class BookForm (forms.Form):
    title = forms.CharField(
        max_length=70, widget=forms.TextInput(attrs={'maxlength': 70}))
    description = forms.CharField(
        max_length=200, widget=forms.Textarea(attrs={'maxlength': 200}))
