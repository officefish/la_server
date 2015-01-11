__author__ = 'inozemcev'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'card.views.cards_list', name='cards_list'),
    url(r'^create/$', 'card.views.create_card', name='create_card'),
    url(r'^edit/(?P<card_id>\d+)/$', 'card.views.edit_card', name='edit_card'),
    url(r'^delete/(?P<card_id>\d+)/$', 'card.views.delete_card', name='delete_card'),
    url(r'^create_eptitude/(?P<card_id>\d+)/$', 'card.views.create_eptitude', name='create_eptitude'),
    url(r'^edit_eptitude/(?P<card_id>\d+)/(?P<eptitude_id>\d+)/$', 'card.views.edit_eptitude', name='edit_eptitude'),
    url(r'^delete_eptitude/(?P<card_id>\d+)/(?P<eptitude_id>\d+)/$', 'card.views.delete_eptitude', name='delete_eptitude'),
    url(r'^create_race/(?P<card_id>\d+)/$', 'card.views.create_race', name='create_race'),
    url(r'^create_subrace/(?P<card_id>\d+)/$', 'card.views.create_subrace', name='create_subrace'),
    url(r'^edit_race/(?P<race_id>\d+)/$', 'card.views.edit_race', name ='edit_race'),
    url(r'^races/$', 'card.views.races_list', name='races_list'),
    url(r'^create_card_for_book/(?P<book_id>\d+)/$', 'card.views.create_card_for_book', name ='create_card_for_book'),
    url(r'^edit_card_for_book/(?P<card_id>\d+)/(?P<book_id>\d+)$', 'card.views.edit_card_for_book', name='edit_card_for_book'),
    url(r'^delete_card_for_book/(?P<card_id>\d+)/(?P<book_id>\d+)$', 'card.views.delete_card_for_book', name='delete_card_for_book'),
    url(r'^create_eptitude_for_book_card/(?P<card_id>\d+)/(?P<book_id>\d+)$', 'card.views.create_eptitude_for_book_card', name='create_eptitude_for_book_card'),
    url(r'^edit_eptitude_for_book_card/(?P<card_id>\d+)/(?P<eptitude_id>\d+)/(?P<book_id>\d+)$', 'card.views.edit_eptitude_for_book_card', name='edit_eptitude_for_book_card'),
    url(r'^delete_eptitude_for_book_card/(?P<card_id>\d+)/(?P<eptitude_id>\d+)/(?P<book_id>\d+)$', 'card.views.delete_eptitude_for_book_card', name='delete_eptitude_for_book_card'),

    )