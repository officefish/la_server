from django.shortcuts import render
from django.template.response import TemplateResponse, HttpResponse
from django.http import HttpResponseRedirect
from group.forms import GroupForm
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import get_current_site
from group.models import Group
from card.models import Card

def create_group (request,
                  card_id,
                  group_form = GroupForm,
                  template_name = 'group/create_group.html'
                  ):

     card = get_object_or_404(Card, pk=card_id)

     redirect_to = "/cards/edit/%s" % card_id

     if request.method == "POST":
        form = group_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']

            group = Group.objects.create(title=title, description=description)

            return HttpResponseRedirect(redirect_to)
     else:
        form = group_form()

     context = {
            'form': form,

     }

     return TemplateResponse(request, template_name, context)

# Create your views here.
