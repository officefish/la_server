from django.shortcuts import render
from hero.models import Hero
from hero.forms import HeroForm
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


def heroes_list(request,
                template_name='hero/heroes_list.html'
                ):

    heroes = Hero.objects.all()

    context = {
        'heroes': heroes,

    }

    return TemplateResponse(request, template_name, context)


def create_hero(request,
                hero_form=HeroForm,
                template_name='hero/create_hero.html'
                ):

    redirect_to = '/heroes'

    if request.method == 'POST':
        form = hero_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            vocation = request.POST['vocation']
            description = request.POST['description']
            health = request.POST['health']
            uid = request.POST['uid']

            hero = Hero.objects.create(
                title=title,
                vocation=vocation,
                description=description,
                uid=uid,
                health=health
            )

            return HttpResponseRedirect(redirect_to)

    else:
        form = hero_form()

    context = {
        'form': form,
    }

    return TemplateResponse(request, template_name, context)


def edit_hero(request, hero_id,
              template_name='hero/edit_hero.html',
              hero_form=HeroForm,
              ):

    redirect_to = '/heroes'

    hero = get_object_or_404(Hero, pk=hero_id)

    data = {
        'title': hero.title,
        'vocation': hero.vocation,
        'description': hero.description,
        'health': hero.health,
        'uid': hero.uid
    }

    if request.method == 'POST':
        form = hero_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            vocation = request.POST['vocation']
            description = request.POST['description']
            health = request.POST['health']
            uid = request.POST['uid']

            hero.title = title
            hero.uid = uid
            hero.vocation = vocation
            hero.description = description
            hero.health = health
            hero.save()

            return HttpResponseRedirect(redirect_to)
    else:
        form = hero_form(data)

    context = {
        'form': form,

    }

    return TemplateResponse(request, template_name, context)


def delete_hero(request, hero_id):
    hero = get_object_or_404(Hero, pk=hero_id)
    hero.delete()
    redirect_to = '/heroes'

    return HttpResponseRedirect(redirect_to)
