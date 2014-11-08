__author__ = 'inozemcev'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'card.views.cards_list', name='cards_list'),
    url(r'^create/$', 'card.views.create_card', name='create_card'),
    url(r'^edit/(?P<card_id>\d+)/$', 'card.views.edit_card', name='edit_card'),
    url(r'^delete/(?P<card_id>\d+)/$', 'card.views.delete_card', name='delete_card'),
    )