__author__ = 'inozemcev'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'book.views.books_list', name='books_list'),
                       url(r'^create/$', 'book.views.create_book',
                           name='create_book'),
                       url(r'^edit_book/(?P<book_id>\d+)/$',
                           'book.views.edit_book', name='edit_book'),
                       url(r'^book/(?P<book_id>\d+)/$',
                           'book.views.book_cards', name='book'),
                       url(r'^add_book_owner/(?P<book_id>\d+)/$',
                           'book.views.add_book_owner', name='add_book_owner'),
                       url(r'^remove_book_owner/(?P<book_id>\d+)/(?P<hero_id>\d+)/$',
                           'book.views.remove_book_owner', name='remove_book_owner'),
                       url(r'^delete_book/(?P<book_id>\d+)/$',
                           'book.views.delete_book', name='delete_book'),
                       )
