__author__ = 'inozemcev'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'card.views.cards_list', name='cards_list'),
    url(r'^get_deck_list/$', 'api.views.getDeckList'),
    url(r'^select_deck/$', 'api.views.selectDeck'),
    )
