# Create your views here.
from django.template.response import TemplateResponse, HttpResponse
from django.http import HttpResponseRedirect
from card.models import Card, CardEptitude, Race, SubRace
from card.forms import CardForm, EptitudeForm, RaceForm, SubRaceForm
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import get_current_site
from book.models import Book


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
            type = int(request.POST["type"])
            auxiliary = bool(int(request.POST["auxiliary"]))
            has_weapon = bool(int(request.POST["has_weapon"]))

            race_id = request.POST['race']
            try :
                race = Race.objects.get(pk=race_id)
            except Race.DoesNotExist:
                race = None

            subrace_id = request.POST['subrace']
            try:
                subrace = SubRace.objects.get(pk=subrace_id)
            except SubRace.DoesNotExist:
                subrace = None

            card = Card.objects.create(
                title=title,
                attack=attack,
                health=health,
                price=price,
                description = description,
                type = type,
                race = race,
                subrace = subrace,
                auxiliary = auxiliary,
                has_weapon = has_weapon

            )

            if 'create_eptitude' in request.POST:
                redirect_to = "/cards/create_eptitude/%s" % card.id

            if 'create_race' in request.POST:
                redirect_to = '/cards/create_race/%s' % card.id

            if 'create_subrace' in request.POST:
                redirect_to = '/cards/create_subrace/%s' % card.id

            return HttpResponseRedirect(redirect_to)

    else:
        data = {"type":2}
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

    try:
        race_id =Race.objects.get (pk=card.race.id).id
    except ValueError:
        race_id = -1
    except AttributeError:
        race_id = -1

    try:
        subrace_id =SubRace.objects.get (pk=card.subrace.id).id
    except ValueError:
        subrace_id = -1
    except AttributeError:
        subrace_id = -1

    try:
        book_id = Book.objects.get (pk=card.book.id).id
    except ValueError:
        book_id = -1
    except AttributeError:
        book_id = -1

    data = {
        "title":card.title,
        "attack":card.attack,
        "health":card.health,
        "price":card.price,
        "description":card.description,
        "type":int(card.type),
        "auxiliary":int(card.auxiliary),
        "race": race_id,
        "book":book_id,
        "subrace":subrace_id,
        "has_weapon":int(card.has_weapon)
    }

    if request.method == "POST":
        form = card_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            attack = request.POST['attack']
            health = request.POST['health']
            price = request.POST['price']
            description = request.POST["description"]
            type = int(request.POST["type"])
            book_id = request.POST['book']
            has_weapon = bool(int(request.POST["has_weapon"]))


            race_id = request.POST['race']
            try :
                race = Race.objects.get(pk=race_id)
            except Race.DoesNotExist:
                race = None

            subrace_id = request.POST['subrace']
            try:
                subrace = SubRace.objects.get(pk=subrace_id)
            except SubRace.DoesNotExist:
                subrace = None

            try:
                book = Book.objects.get(pk=book_id)
            except Book.DoesNotExist:
                book = None

            card.title = title
            card.attack = attack
            card.health = health
            card.price = price
            card.description = description
            card.type = type
            card.race = race
            card.subrace = subrace
            card.auxiliary = bool(int(request.POST["auxiliary"]))
            card.book = book
            card.has_weapon = has_weapon
            card.save()

            if 'create_eptitude' in request.POST:
                redirect_to = "/cards/create_eptitude/%s" % card.id

            if 'create_race' in request.POST:
                redirect_to = '/cards/create_race/%s' % card.id

            if 'create_subrace' in request.POST:
                redirect_to = '/cards/create_subrace/%s' % card.id


            return HttpResponseRedirect(redirect_to)
    else:
        form = card_form(data)

    context = {
        'form': form,
        'card':card,
        'eptitudes': card.eptitudes,
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

def create_eptitude (
       request,card_id,
       eptitude_form = EptitudeForm,
       template_name='card/create_eptitude.html'):

    card = get_object_or_404(Card, pk=card_id)

    redirect_to = "/cards/edit/%s" % card_id

    if request.method == "POST":
        form = eptitude_form(card, request.POST)
        if form.is_valid():

            period = request.POST['period']
            level = request.POST['level']
            type = request.POST['type']
            power = request.POST["power"]
            lifecycle = request.POST['lifecycle']
            attachment = request.POST['attachment']
            condition = request.POST['condition']
            try:
                dynamic = bool(int(request.POST["dynamic"]))
            except:
                dynamic = 0

            try:
                attach_hero = bool(int(request.POST["attach_hero"]))
            except:
                attach_hero = 0

            try:
                attach_initiator = bool(int(request.POST["attach_initiator"]))
            except:
                attach_initiator = 0


            race_id = request.POST['race']
            try :
                race = Race.objects.get(pk=race_id)
            except Race.DoesNotExist:
                race = None

            subrace_id = request.POST['subrace']
            try:
                subrace = SubRace.objects.get(pk=subrace_id)
            except SubRace.DoesNotExist:
                subrace = None

            unit_id = request.POST['unit']
            try :
                unit = Card.objects.get(pk=unit_id)
            except Card.DoesNotExist:
                unit = None


            dependency_id = request.POST['dependency']
            try :
                dependency = CardEptitude.objects.get(pk=int(dependency_id))
            except CardEptitude.DoesNotExist:
                dependency = None

            CardEptitude.objects.create(
                card = card,
                period = period,
                level = level,
                type = type,
                power = power,
                lifecycle = lifecycle,
                race = race,
                subrace = subrace,
                unit = unit,
                dependency = dependency,
                condition = condition,
                dynamic = dynamic,
                attachment = attachment,
                attach_hero = attach_hero,
                attach_initiator = attach_initiator
            )


            return HttpResponseRedirect(redirect_to)
    else:
        form = eptitude_form(card)



    current_site = get_current_site(request)

    context = {
        'form': form,
        'site': current_site,
        'card': card,
        'site_name': current_site.name,
    }


    return TemplateResponse(request, template_name, context)

def edit_eptitude (
        request, card_id, eptitude_id,
        eptitude_form = EptitudeForm,
        template_name='card/edit_eptitude.html'):

     card = get_object_or_404(Card, pk=card_id)

     redirect_to = "/cards/edit/%s" % card_id

     eptitude = get_object_or_404(CardEptitude, pk=eptitude_id)

     if request.method == "POST":
        form = eptitude_form(card, request.POST)
        if form.is_valid():

            period = request.POST['period']
            level = request.POST['level']
            type = request.POST['type']
            power = request.POST["power"]
            attachment = request.POST["attachment"]
            condition = request.POST['condition']
            lifecycle = request.POST['lifecycle']
            try:
                dynamic = bool(int(request.POST["dynamic"]))
            except:
                dynamic = 0

            try:
                attach_hero = bool(int(request.POST["attach_hero"]))
            except:
                attach_hero = 0

            try:
                attach_initiator = bool(int(request.POST["attach_initiator"]))
            except:
                attach_initiator = 0

            race_id = request.POST['race']
            try :
                race = Race.objects.get(pk=race_id)
            except Race.DoesNotExist:
                race = None

            subrace_id = request.POST['subrace']
            try:
                subrace = SubRace.objects.get(pk=subrace_id)
            except SubRace.DoesNotExist:
                subrace = None

            unit_id = request.POST['unit']
            try :
                unit = Card.objects.get(pk=unit_id)
            except Card.DoesNotExist:
                unit = None

            dependency_id = request.POST['dependency']
            try :
                dependency = CardEptitude.objects.get(pk=int(dependency_id))
            except CardEptitude.DoesNotExist:
                dependency = None

            eptitude.period = period
            eptitude.level = level
            eptitude.type = type
            eptitude.power = power
            eptitude.lifecycle = lifecycle
            eptitude.condition = condition
            eptitude.race = race
            eptitude.subrace = subrace
            eptitude.unit = unit
            eptitude.dependency = dependency
            eptitude.dynamic = dynamic
            eptitude.attach_hero = attach_hero
            eptitude.attach_initiator = attach_initiator
            eptitude.attachment = attachment

            eptitude.save()

            return HttpResponseRedirect(redirect_to)

     else:


        try:
                race_id =Race.objects.get (pk=eptitude.race.id).id
        except ValueError:
                race_id = -1
        except AttributeError:
                race_id = -1

        try:
              subrace_id =SubRace.objects.get (pk=eptitude.subrace.id).id
        except ValueError:
              subrace_id = -1
        except AttributeError:
              subrace_id = -1

        try:
              unit_id =Card.objects.get (pk=eptitude.unit.id).id
        except ValueError:
              unit_id = -1
        except AttributeError:
              unit_id = -1

        try :
            dependency_id = card.eptitudes.get(pk=int(eptitude.dependency.id)).id
        except ValueError:
            dependency_id = -1
        except AttributeError:
            dependency_id = -1


        data = {
            "period":eptitude.period,
            "level":eptitude.level,
            "type":eptitude.type,
            "power":eptitude.power,
            "race":race_id,
            "subrace":subrace_id,
            "unit":unit_id,
            "dependency":dependency_id,
            "lifecycle":eptitude.lifecycle,
            "condition":eptitude.condition,
            'dynamic':int(eptitude.dynamic),
            'attachment':eptitude.attachment,
            'attach_hero':int(eptitude.attach_hero),
            'attach_initiator':int(eptitude.attach_initiator)
        }
        form = eptitude_form(card, data)

     current_site = get_current_site(request)

     context = {
            'form': form,
            'card': card,
            'site': current_site,
            'site_name': current_site.name,
        }


     return TemplateResponse(request, template_name, context)

def delete_eptitude (request, card_id, eptitude_id):

     redirect_to = "/cards/edit/%s" % card_id
     eptitude = get_object_or_404(CardEptitude, pk=eptitude_id)
     eptitude.delete()

     return HttpResponseRedirect(redirect_to)

def create_race (request,
                 card_id,
                 race_form = RaceForm,
                 template_name = 'card/create_race.html'
):

     card = get_object_or_404(Card, pk=card_id)

     redirect_to = "/cards/edit/%s" % card_id

     if request.method == "POST":
        form = race_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST["description"]

            Race.objects.create(title=title, description=description)

            return HttpResponseRedirect(redirect_to)
     else:
        form = race_form()

     current_site = get_current_site(request)

     context = {
            'form': form,
            'site': current_site,
            'site_name': current_site.name,
        }


     return TemplateResponse(request, template_name, context)

def create_subrace (request,
                 card_id,
                 subrace_form = SubRaceForm,
                 template_name = 'card/create_subrace.html'
):

     card = get_object_or_404(Card, pk=card_id)

     redirect_to = "/cards/edit/%s" % card_id

     if request.method == "POST":
        form = subrace_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST["description"]
            race_id = request.POST['race']
            race = Race.objects.get(pk=race_id)

            SubRace.objects.create(title=title, description=description, race=race)

            return HttpResponseRedirect(redirect_to)
     else:
        form = subrace_form()

     current_site = get_current_site(request)

     context = {
            'form': form,
            'site': current_site,
            'site_name': current_site.name,
        }


     return TemplateResponse(request, template_name, context)

def edit_race (request, race_id,
                 book_form = RaceForm,
                 template_name = 'card/edit_race.html'
                 ):

     race = get_object_or_404(Race, pk=race_id)

     data = {
         "title":race.title,
         "description":race.description
     }

     redirect_to = "/cards/races"

     if request.method == "POST":
        form = book_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']

            race.title=title
            race.description = description
            race.save()
            return HttpResponseRedirect(redirect_to)
     else:
        form = book_form(data)

     context = {
            'form': form,
            'race':race,

     }

     return TemplateResponse(request, template_name, context)

def races_list (
        request,
        template_name = 'card/races_list.html'):

    races = Race.objects.all()

    context = {
        'races': races,
    }

    return TemplateResponse(request, template_name, context)

# book functions

def delete_card_for_book(
        request,card_id, book_id
        ):

    book = get_object_or_404(Book, pk=book_id)
    redirect_to = "/books/book/%s" % book_id

    card = get_object_or_404(Card, pk=card_id)
    card_title = card.title
    card.delete()

    context = {
        'card_title': card_title
    }

    return HttpResponseRedirect(redirect_to)


def create_card_for_book (request, book_id,
         template_name='card/create_card.html',
         card_form=CardForm,
         current_app=None,
         extra_context=None):

    book = get_object_or_404(Book, pk=book_id)

    redirect_to = "/books/book/%s" % book_id

    if request.method == "POST":
        form = card_form(request.POST)
        if form.is_valid():

            title = request.POST['title']
            attack = request.POST['attack']
            health = request.POST['health']
            price = request.POST['price']
            description = request.POST["description"]
            type = int(request.POST["type"])
            race_id = request.POST['race']
            book_id = request.POST['book']
            auxiliary = bool(int(request.POST["auxiliary"]))
            has_weapon = bool(int(request.POST["has_weapon"]))


            try :
                race = Race.objects.get(pk=race_id)
            except Race.DoesNotExist:
                race = None

            subrace_id = request.POST['subrace']
            try:
                subrace = SubRace.objects.get(pk=subrace_id)
            except SubRace.DoesNotExist:
                subrace = None

            try:
                book =Book.objects.get (pk=book_id)
            except Book.DoesNotExist:
                book = None


            card = Card.objects.create(
                title=title,
                attack=attack,
                health=health,
                price=price,
                description = description,
                type = type,
                race = race,
                subrace = subrace,
                auxiliary = auxiliary,
                book = book,
                has_weapon = has_weapon
            )

            if 'create_eptitude' in request.POST:
                redirect_to = "/cards/create_eptitude_for_book_card/%s/%s" % (card.id, book.id)

            if 'create_race' in request.POST:
                redirect_to = '/cards/create_race/%s' % card.id

            if 'create_subrace' in request.POST:
                redirect_to = '/cards/create_subrace/%s' % card.id

            return HttpResponseRedirect(redirect_to)

    else:
        data = {"type":2,
               "book":book.id,
        }
        form = card_form(data)



    current_site = get_current_site(request)

    context = {
        'form': form,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

def edit_card_for_book (request,card_id, book_id,
         template_name='card/edit_card_for_book.html',
         card_form=CardForm,
         current_app=None,
         extra_context=None):

    card = get_object_or_404(Card, pk=card_id)
    book = get_object_or_404(Book, pk=book_id)
    redirect_to = "/books/book/%s" % book_id

    try:
        race_id =Race.objects.get (pk=card.race.id).id
    except ValueError:
        race_id = -1
    except AttributeError:
        race_id = -1

    try:
        subrace_id =SubRace.objects.get (pk=card.subrace.id).id
    except ValueError:
        subrace_id = -1
    except AttributeError:
        subrace_id = -1

    try:
        book_id = Book.objects.get (pk=card.book.id).id
    except ValueError:
        book_id = -1
    except AttributeError:
        book_id = -1

    data = {
        "title":card.title,
        "attack":card.attack,
        "health":card.health,
        "price":card.price,
        "description":card.description,
        "type":int(card.type),
        "auxiliary":int(card.auxiliary),
        "race": race_id,
        "book":book_id,
        "subrace":subrace_id,
        "has_weapon":int(card.has_weapon)
    }

    if request.method == "POST":
        form = card_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            attack = request.POST['attack']
            health = request.POST['health']
            price = request.POST['price']
            description = request.POST["description"]
            type = int(request.POST["type"])
            book_id = request.POST['book']
            has_weapon = bool(int(request.POST["has_weapon"]))

            race_id = request.POST['race']
            try :
                race = Race.objects.get(pk=race_id)
            except Race.DoesNotExist:
                race = None

            subrace_id = request.POST['subrace']
            try:
                subrace = SubRace.objects.get(pk=subrace_id)
            except SubRace.DoesNotExist:
                subrace = None

            try:
                book = Book.objects.get(pk=book_id)
            except Book.DoesNotExist:
                book = None

            card.title = title
            card.attack = attack
            card.health = health
            card.price = price
            card.description = description
            card.type = type
            card.race = race
            card.subrace = subrace
            card.auxiliary = bool(int(request.POST["auxiliary"]))
            card.book = book
            card.has_weapon = has_weapon
            card.save()

            if 'create_eptitude' in request.POST:
                redirect_to = "/cards/create_eptitude_for_book_card/%s/%s" % (card.id, book.id)

            if 'create_race' in request.POST:
                redirect_to = '/cards/create_race/%s' % card.id

            if 'create_subrace' in request.POST:
                redirect_to = '/cards/create_subrace/%s' % card.id


            return HttpResponseRedirect(redirect_to)
    else:
        form = card_form(data)

    context = {
        'form': form,
        'card':card,
        'eptitudes': card.eptitudes,
        'book':book,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

def create_eptitude_for_book_card (
       request,card_id, book_id,
       eptitude_form = EptitudeForm,
       template_name='card/create_eptitude.html'):

    card = get_object_or_404(Card, pk=card_id)
    book = get_object_or_404(Book, pk=book_id)
    redirect_to = "/cards/edit_card_for_book/%s/%s" % (card_id, book_id)

    if request.method == "POST":
        form = eptitude_form(card, request.POST)
        if form.is_valid():

            period = request.POST['period']
            level = request.POST['level']
            type = request.POST['type']
            power = request.POST["power"]
            lifecycle = request.POST['lifecycle']
            condition = request.POST['condition']
            attachment = request.POST['attachment']
            try:
                dynamic = bool(int(request.POST["dynamic"]))
            except:
                dynamic = 0

            try:
                attach_hero = bool(int(request.POST["attach_hero"]))
            except:
                attach_hero = 0

            try:
                attach_initiator = bool(int(request.POST["attach_initiator"]))
            except:
                attach_initiator = 0

            race_id = request.POST['race']
            try :
                race = Race.objects.get(pk=race_id)
            except Race.DoesNotExist:
                race = None

            subrace_id = request.POST['subrace']
            try:
                subrace = SubRace.objects.get(pk=subrace_id)
            except SubRace.DoesNotExist:
                subrace = None

            unit_id = request.POST['unit']
            try :
                unit = Card.objects.get(pk=unit_id)
            except Card.DoesNotExist:
                unit = None


            dependency_id = request.POST['dependency']
            try :
                dependency = CardEptitude.objects.get(pk=int(dependency_id))
            except CardEptitude.DoesNotExist:
                dependency = None

            CardEptitude.objects.create(
                card = card,
                period = period,
                level = level,
                type = type,
                power = power,
                lifecycle = lifecycle,
                race = race,
                subrace = subrace,
                unit = unit,
                dependency = dependency,
                condition = condition,
                dynamic = dynamic,
                attachment = attachment,
                attach_hero = attach_hero,
                attach_initiator = attach_initiator
            )


            return HttpResponseRedirect(redirect_to)
    else:
        form = eptitude_form(card)



    current_site = get_current_site(request)

    context = {
        'form': form,
        'site': current_site,
        'card': card,
        'site_name': current_site.name,
    }


    return TemplateResponse(request, template_name, context)

def edit_eptitude_for_book_card (
        request, card_id, eptitude_id, book_id,
        eptitude_form = EptitudeForm,
        template_name='card/edit_eptitude.html'):

     card = get_object_or_404(Card, pk=card_id)
     book = get_object_or_404(Book, pk=book_id)
     redirect_to = "/cards/edit_card_for_book/%s/%s" % (card_id, book_id)

     eptitude = get_object_or_404(CardEptitude, pk=eptitude_id)

     if request.method == "POST":
        form = eptitude_form(card, request.POST)
        if form.is_valid():

            period = request.POST['period']
            level = request.POST['level']
            type = request.POST['type']
            power = request.POST["power"]
            attachment = request.POST["attachment"]
            condition = request.POST['condition']
            lifecycle = request.POST['lifecycle']
            try:
                dynamic = bool(int(request.POST["dynamic"]))
            except:
                dynamic = 0

            try:
                attach_hero = bool(int(request.POST["attach_hero"]))
            except:
                attach_hero = 0

            try:
                attach_initiator = bool(int(request.POST["attach_initiator"]))
            except:
                attach_initiator = 0


            race_id = request.POST['race']
            try :
                race = Race.objects.get(pk=race_id)
            except Race.DoesNotExist:
                race = None

            subrace_id = request.POST['subrace']
            try:
                subrace = SubRace.objects.get(pk=subrace_id)
            except SubRace.DoesNotExist:
                subrace = None

            unit_id = request.POST['unit']
            try :
                unit = Card.objects.get(pk=unit_id)
            except Card.DoesNotExist:
                unit = None

            dependency_id = request.POST['dependency']
            try :
                dependency = CardEptitude.objects.get(pk=int(dependency_id))
            except CardEptitude.DoesNotExist:
                dependency = None

            eptitude.period = period
            eptitude.level = level
            eptitude.type = type
            eptitude.power = power
            eptitude.lifecycle = lifecycle
            eptitude.condition = condition
            eptitude.race = race
            eptitude.subrace = subrace
            eptitude.unit = unit
            eptitude.dependency = dependency
            eptitude.dynamic = dynamic
            eptitude.attachment = attachment
            eptitude.attach_hero = attach_hero
            eptitude.attach_initiator = attach_initiator

            eptitude.save()

            return HttpResponseRedirect(redirect_to)

     else:


        try:
                race_id =Race.objects.get (pk=eptitude.race.id).id
        except ValueError:
                race_id = -1
        except AttributeError:
                race_id = -1

        try:
              subrace_id =SubRace.objects.get (pk=eptitude.subrace.id).id
        except ValueError:
              subrace_id = -1
        except AttributeError:
              subrace_id = -1

        try:
              unit_id =Card.objects.get (pk=eptitude.unit.id).id
        except ValueError:
              unit_id = -1
        except AttributeError:
              unit_id = -1

        try :
            dependency_id = card.eptitudes.get(pk=int(eptitude.dependency.id)).id
        except ValueError:
            dependency_id = -1
        except AttributeError:
            dependency_id = -1

        data = {
            "period":eptitude.period,
            "level":eptitude.level,
            "type":eptitude.type,
            "power":eptitude.power,
            "race":race_id,
            "subrace":subrace_id,
            "unit":unit_id,
            "dependency":dependency_id,
            "lifecycle":eptitude.lifecycle,
            "condition":eptitude.condition,
            "dynamic":int(eptitude.dynamic),
            'attachment':eptitude.attachment,
            'attach_hero':int(eptitude.attach_hero),
            'attach_initiator':int(eptitude.attach_initiator)
        }
        form = eptitude_form(card, data)

     current_site = get_current_site(request)

     context = {
            'form': form,
            'card': card,
            'site': current_site,
            'site_name': current_site.name,
        }


     return TemplateResponse(request, template_name, context)

def delete_eptitude_for_book_card (request, card_id, eptitude_id, book_id):

     book = get_object_or_404(Book, pk=book_id)
     redirect_to = "/cards/edit_card_for_book/%s/%s" % (card_id, book_id)
     eptitude = get_object_or_404(CardEptitude, pk=eptitude_id)
     eptitude.delete()

     return HttpResponseRedirect(redirect_to)










