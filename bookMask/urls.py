__author__ = 'inozemcev'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^book/(?P<book_id>\d+)$',
                           'bookMask.views.book_cards_mask', name='book_mask'),
                       url(r'^edit_item/book/(?P<book_id>\d+)/item/(?P<item_id>\d+)',
                           'bookMask.views.edit_book_mask_item', name='edit_book_mask_item'),

                       )
