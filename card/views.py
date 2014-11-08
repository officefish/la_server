# Create your views here.
from django.template.response import TemplateResponse, HttpResponse
from django.http import HttpResponseRedirect
from card.models import Card
from card.forms import CardForm
from django.shortcuts import get_object_or_404

def cards_list (
        request,
        template_name = 'card/cards_list.html'):

    _cards = Card.objects.all().order_by('price')

    context = {
        'cards': _cards,
    }

    return TemplateResponse(request, template_name, context)


def create_card (request,
         template_name='card/create_card.html',
         card_form=CardForm,
         current_app=None,
         extra_context=None):

    redirect_to = "/cards"

    if request.method == "POST":
        form = card_form(request.POST)
        if form.is_valid():

            title = request.POST['title']
            attack = request.POST['attack']
            health = request.POST['health']
            price = request.POST['price']
            description = request.POST["description"]
            type = bool(int(request.POST["type"]))

            card = Card.objects.create(
                title=title,
                attack=attack,
                health=health,
                price=price,
                description = description,
                type = type,

            )

            return HttpResponseRedirect(redirect_to)

    else:
        data = {"type":1}
        form = card_form(data)

    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)



def edit_card (request,card_id,
         template_name='card/edit_card.html',
         card_form=CardForm,
         current_app=None,
         extra_context=None):

    redirect_to = "/cards"

    card = get_object_or_404(Card, pk=card_id)

    data = {
        "title":card.title,
        "attack":card.attack,
        "health":card.health,
        "price":card.price,
        "description":card.description,
        "type":int(card.type),
        "auxiliary":int(card.auxiliary)
    }

    if request.method == "POST":
        form = card_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            attack = request.POST['attack']
            health = request.POST['health']
            price = request.POST['price']
            description = request.POST["description"]
            type = bool(int(request.POST["type"]))

            card.title = title
            card.attack = attack
            card.health = health
            card.price = price
            card.description = description
            card.type = type
            card.auxiliary = bool(int(request.POST["auxiliary"]))
            card.save()

            return HttpResponseRedirect(redirect_to)
    else:
        form = card_form(data)

    context = {
        'form': form,
        'card':card,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def delete_card(
        request,card_id,
        ):

    redirect_to = "/cards"

    card = get_object_or_404(Card, pk=card_id)
    card_title = card.title
    card.delete()

    context = {
        'card_title': card_title
    }

    return HttpResponseRedirect(redirect_to)