__author__ = 'inozemcev'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^crossdomain.xml$', 'api.views.crossdomain', name='crossdomain'),
    url(r'^$', 'card.views.cards_list', name='cards_list'),
    url(r'^get_deck_list/$', 'api.views.getDeckList'),
    url(r'^get_collection/$', 'api.views.getCollection'),
    url(r'^get_heroes/$', 'api.views.getHeroes'),
    url(r'^select_deck/$', 'api.views.selectDeck'),
    url(r'create_deck/$', 'api.views.createDeck'),
    url(r'save_deck/$', 'api.views.saveDeck'),
    url(r'remove_deck/$', 'api.views.removeDeck'),
    url(r'edit_deck/$', 'api.views.editDeck'),
    url(r'^get_full_collection/$', 'api.views.getFullCollection'),
    url(r'^craft_card/$', 'api.views.craftCard'),
    url(r'^destroy_card/$', 'api.views.destroyCard'),
    url(r'^achieves_list/$', 'api.views.getAchievesList'),
    url(r'^setup_achieves/$', 'api.views.setupAchieves'),
    url(r'^craft_achieves_list/$', 'api.views.craftAchievesList'),
    url(r'^craft_achieve/$', 'api.views.craftAchieve'),
    url(r'^destroy_achieve/$', 'api.views.destroyAchieve'),
    url(r'^update_heroes/$', 'api.views.updateHeroes'),
    )
