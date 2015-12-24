from django.shortcuts import render

from weapon.models import Weapon
from weapon.forms import WeaponForm
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

# Create your views here.


def weapon_list(request,
                template_name='weapon/weapons_list.html'
                ):

    weapons = Weapon.objects.all()

    context = {
        'weapons': weapons,
    }
    return TemplateResponse(request, template_name, context)


def create_weapon(request,
                  weapon_form=WeaponForm,
                  template_name='weapon/create_weapon.html'
                  ):

    redirect_to = '/weapons'

    if request.method == 'POST':
        form = weapon_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            power = request.POST['power']
            strength = request.POST['strength']

            weapon = Weapon.objects.create(
                title=title,
                description=description,
                power=power,
                strength=strength
            )

            return HttpResponseRedirect(redirect_to)

    else:
        form = weapon_form()

    context = {
        'form': form,
    }

    return TemplateResponse(request, template_name, context)


def edit_weapon(request, weapon_id,
                template_name='weapon/edit_weapon.html',
                weapon_form=WeaponForm,
                ):

    redirect_to = '/weapons'

    weapon = get_object_or_404(Weapon, pk=weapon_id)

    data = {
        'title': weapon.title,
        'description': weapon.description,
        'power': weapon.power,
        'strength': weapon.strength
    }

    if request.method == 'POST':
        form = weapon_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            power = request.POST['power']
            strength = request.POST['strength']

            weapon.title = title
            weapon.description = description
            weapon.power = power
            weapon.strength = strength
            weapon.save()

            return HttpResponseRedirect(redirect_to)
    else:
        form = weapon_form(data)

    context = {
        'form': form,

    }

    return TemplateResponse(request, template_name, context)


def delete_weapon(request, weapon_id):
    weapon = get_object_or_404(Weapon, pk=weapon_id)
    weapon.delete()
    redirect_to = '/weapons'

    return HttpResponseRedirect(redirect_to)
