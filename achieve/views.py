from django.shortcuts import render
from achieve.models import Achieve, AchieveCollector, AchieveMask
from django.template.response import TemplateResponse, HttpResponse
from achieve.forms import AchieveForm, AddAchieveOwnerForm
from django.http import HttpResponseRedirect
from hero.models import Hero
from django.shortcuts import get_object_or_404
from achieve.forms import AchieveMaskForm

# Create your views here.


def achieve_list(
        request,
        template_name='achieve/achieve_list.html'):

    _achieves = Achieve.objects.all().order_by('price')

    context = {
        'achieves': _achieves,
    }

    return TemplateResponse(request, template_name, context)


def create_achieve(request,
                   template_name='achieve/create_achieve.html',
                   achieve_form=AchieveForm,
                   current_app=None,
                   extra_context=None):

    redirect_to = '/achieves'

    if request.method == 'POST':
        form = achieve_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            price = request.POST['price']
            type = int(request.POST['type'])
            autonomic = bool(int(request.POST['autonomic']))

            achieve = Achieve.objects.create(
                title=title,
                price=price,
                description=description,
                type=type,
                autonomic=autonomic
            )

            if 'add_achieve_owner' in request.POST:
                redirect_to = '/achieves/add_achieve_owner/%s' % achieve.id

            if 'create_eptitude' in request.POST:
                redirect_to = '/cards/create_eptitude_for_achieve/%s' % (
                    achieve.id)

            return HttpResponseRedirect(redirect_to)

    else:
        data = {'type': 0, 'autonomic': 0}
        form = achieve_form(data)

    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def edit_achieve(request, achieve_id,
                 template_name='achieve/edit_achieve.html',
                 achieve_form=AchieveForm,
                 current_app=None,
                 extra_context=None):

    achieve = get_object_or_404(Achieve, pk=achieve_id)

    data = {
        'title': achieve.title,
        'description': achieve.description,
        'type': int(achieve.type),
        'autonomic': int(achieve.autonomic),
        'price': int(achieve.price)
    }

    redirect_to = '/achieves'

    if request.method == 'POST':
        form = achieve_form(request.POST)
        if form.is_valid():
            achieve.title = request.POST['title']
            achieve.description = request.POST['description']
            achieve.price = request.POST['price']
            achieve.type = int(request.POST['type'])
            achieve.autonomic = bool(int(request.POST['autonomic']))
            achieve.save()

            if 'add_achieve_owner' in request.POST:
                redirect_to = '/achieves/add_achieve_owner/%s' % achieve.id

            if 'create_eptitude' in request.POST:
                redirect_to = '/cards/create_eptitude_for_achieve/%s' % (
                    achieve.id)

            return HttpResponseRedirect(redirect_to)

    else:
        form = achieve_form(data)

    context = {
        'form': form,
        'achieve': achieve,
        'eptitudes': achieve.eptitudes
    }

    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def delete_achieve(request, achieve_id):

    achieve = get_object_or_404(Achieve, pk=achieve_id)
    achieve.delete()

    redirect_to = '/achieves/'

    return HttpResponseRedirect(redirect_to)


def add_achieve_owner(request,
                      achieve_id,
                      add_achieve_owner_form=AddAchieveOwnerForm,
                      template_name='achieve/add_achieve_owner.html'
                      ):

    achieve = get_object_or_404(Achieve, pk=achieve_id)

    redirect_to = '/achieves/edit_achieve/%s' % achieve.id

    if request.method == 'POST':
        form = add_achieve_owner_form(request.POST)
        if form.is_valid():

            hero_id = request.POST['hero']
            try:
                hero = Hero.objects.get(pk=hero_id)
                owner = AchieveCollector(owner=hero, achieve=achieve)
                owner.save()

            except Hero.DoesNotExist:
                pass

            return HttpResponseRedirect(redirect_to)
    else:
        form = add_achieve_owner_form()

    context = {
        'form': form,

    }

    return TemplateResponse(request, template_name, context)


def remove_achieve_owner(request,
                         achieve_id,
                         hero_id
                         ):
    achieve = get_object_or_404(Achieve, pk=achieve_id)
    hero = get_object_or_404(Hero, pk=hero_id)

    owner = AchieveCollector.objects.get(owner=hero, achieve=achieve)
    owner.delete()

    redirect_to = '/achieves/edit_achieve/%s' % achieve.id
    return HttpResponseRedirect(redirect_to)


def mask_list(request,
              template_name='achieve/achieve_masks_list.html'):

    _masks = AchieveMask.objects.all()

    context = {
        'slots': _masks,
    }

    return TemplateResponse(request, template_name, context)


def edit_achieve_mask(request, mask_id,
                      mask_item_form=AchieveMaskForm,
                      template_name='achieve/edit_achieve_mask.html'
                      ):

    redirect_to = '/achieves/achieve_masks'

    mask = AchieveMask.objects.get(pk=mask_id)

    if request.method == 'POST':
        form = mask_item_form(request.POST)
        if form.is_valid():

            rarity = request.POST['rarity']
            buy_cost = request.POST['buy_cost']
            sale_cost = request.POST['sale_cost']
            access = request.POST['access']
            max_access = request.POST['max_access']
            craft_available = bool(int(request.POST['craft_available']))

            mask.rarity = rarity
            mask.buy_cost = buy_cost
            mask.sale_cost = sale_cost
            mask.access = access
            mask.craft_available = craft_available
            mask.max_access = max_access
            mask.save()

            return HttpResponseRedirect(redirect_to)

    else:
        data = {
            'rarity': mask.rarity,
            'buy_cost': mask.buy_cost,
            'sale_cost': mask.sale_cost,
            'access': mask.access,
            'max_access': mask.max_access,
            'craft_available': int(mask.craft_available)

        }
        form = mask_item_form(data)

    context = {
        'form': form,
    }
    return TemplateResponse(request, template_name, context)
