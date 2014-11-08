__author__ = 'inozemcev'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'hero.views.heroes_list', name='heroes_list'),
    url(r'^create_hero/$', 'hero.views.create_hero', name ='create_hero'),
    url(r'^edit_hero/(?P<hero_id>\d+)/$', 'hero.views.edit_hero', name ='edit_hero'),
    url(r'^delete_hero/(?P<hero_id>\d+)/$', 'hero.views.delete_hero', name ='delete_hero'),

    )