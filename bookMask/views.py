from django.shortcuts import render
from django.template.response import TemplateResponse, HttpResponse
from django.http import HttpResponseRedirect
from book.models import Book
from bookMask.models import BookMask, MaskItem, MaskCollector
from bookMask.forms import MaskItemForm
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import get_current_site

# Create your views here.
def book_cards_mask (request,
                    book_id,
                    template_name='book/book_mask.html'
                    ):

    book = get_object_or_404(Book, pk=book_id)

    try:
        mask = BookMask.objects.get (book=book)
    except BookMask.DoesNotExist:
        mask = BookMask.objects.create (book=book)

    cards = book.cards.filter(auxiliary=False)

    slots = []
    for card in cards:
        slot = {}
        try:
            maskItem = MaskItem.objects.get(card=card)
        except MaskItem.DoesNotExist:
            maskItem = MaskItem.objects.create(card=card)
            MaskCollector.objects.create(item=maskItem, mask=mask)
        slot['card'] = card
        slot['item'] = maskItem
        slots.append(slot)


    context = {
            'book': book,
            'slots':slots,
    }

    return TemplateResponse(request, template_name, context)

def edit_book_mask_item (request, book_id, item_id,
                         mask_item_form = MaskItemForm,
                         template_name='book/edit_mask_item.html'
                         ):

    book = get_object_or_404(Book, pk=book_id)
    redirect_to = "/mask/book/%s" % book.id

    item = MaskItem.objects.get(pk=item_id)

    if request.method == "POST":
        form = mask_item_form(request.POST)
        if form.is_valid():

            rarity = request.POST['rarity']
            buy_cost = request.POST['buy_cost']
            sale_cost = request.POST['sale_cost']
            access_simple = request.POST['access_simple']
            max_simple = request.POST['max_simple']
            access_golden = request.POST['access_golden']
            max_golden = request.POST['max_golden']
            craft_available = bool(int(request.POST["craft_available"]))

            item.rarity = rarity
            item.buy_cost = buy_cost
            item.sale_cost = sale_cost
            item.access_simple = access_simple
            item.max_simple = max_simple
            item.access_golden = access_golden
            item.max_golden = max_golden
            item.craft_available =  craft_available
            item.save ()

            return HttpResponseRedirect(redirect_to)

    else:
        data = {
            "rarity":item.rarity,
            "buy_cost":item.buy_cost,
            "sale_cost":item.sale_cost,
            "access_simple":item.access_simple,
            "max_simple":item.max_simple,
            "access_golden":item.access_golden,
            "max_golden":item.max_golden,
            "craft_available":int(item.craft_available)

        }
        form = mask_item_form(data)

    context = {
        'form': form,
        'card':item.card,
    }
    return TemplateResponse(request, template_name, context)