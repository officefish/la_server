# Create your views here.
from django.template.response import TemplateResponse, HttpResponse
from django.http import HttpResponseRedirect
from book.forms import BookForm, AddBookOwnerForm
from book.models import Book
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import get_current_site
from hero.models import Hero

def create_book (request,
                 book_form = BookForm,
                 template_name = 'book/create_book.html'
                 ):

     redirect_to = "/books/"

     if request.method == "POST":
        form = book_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']

            book = Book.objects.create(title=title, description=description)

            if 'add_book_owner' in request.POST:
                redirect_to = "/books/add_book_owner/%s" % book.id


            return HttpResponseRedirect(redirect_to)
     else:
        form = book_form()

     context = {
            'form': form,

     }

     return TemplateResponse(request, template_name, context)

def books_list (
        request,
        template_name = 'book/books_list.html'):

    books = Book.objects.all()

    context = {
        'books': books,

    }

    return TemplateResponse(request, template_name, context)

def book_cards (request, book_id,
          template_name = 'book/book.html'
          ):
    book = get_object_or_404(Book, pk=book_id)

    context = {
            'book': book,
            'cards':book.cards,
    }

    return TemplateResponse(request, template_name, context)

def edit_book (request, book_id,
                 book_form = BookForm,
                 template_name = 'book/edit_book.html'
                 ):

     book = get_object_or_404(Book, pk=book_id)

     data = {
         "title":book.title,
         "description":book.description
     }

     redirect_to = "/books/"

     if request.method == "POST":
        form = book_form(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']

            book.title=title
            book.description = description
            book.save()

            if 'add_book_owner' in request.POST:

                redirect_to = "/books/add_book_owner/%s" % book.id


            return HttpResponseRedirect(redirect_to)
     else:
        form = book_form(data)

     context = {
            'form': form,
            'book':book,
     }

     return TemplateResponse(request, template_name, context)

def delete_book (request, book_id):

    book = get_object_or_404(Book, pk=book_id)
    book.delete()

    redirect_to = "/books/"

    return HttpResponseRedirect(redirect_to)


def add_book_owner (request,
                    book_id,
                    add_book_owner_form= AddBookOwnerForm,
                    template_name='book/add_book_owner.html'
                    ):


     book = get_object_or_404(Book, pk=book_id)

     redirect_to = "/books/edit_book/%s" % book.id

     if request.method == "POST":
        form = add_book_owner_form(request.POST)
        if form.is_valid():

            hero_id = request.POST['hero']
            try:
                hero = Hero.objects.get(pk=hero_id)
                book.heroes.add (hero)
            except Hero.DoesNotExist:
                pass

            return HttpResponseRedirect(redirect_to)
     else:
        form = add_book_owner_form ()

     context = {
            'form': form,

     }

     return TemplateResponse(request, template_name, context)

def remove_book_owner (request,
                       book_id,
                       hero_id
                       ):
     book = get_object_or_404(Book, pk=book_id)
     hero = get_object_or_404(Hero, pk=hero_id)

     book.heroes.remove(hero)

     redirect_to = "/cards/edit_book/%s" % book.id
     return HttpResponseRedirect(redirect_to)




