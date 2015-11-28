__author__ = 'inozemcev'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'weapon.views.weapon_list', name='weapons_list'),
    url(r'^create_weapon/$', 'weapon.views.create_weapon', name ='create_weapon'),
    url(r'^edit_weapon/(?P<weapon_id>\d+)/$$', 'weapon.views.edit_weapon', name ='edit_weapon'),
    url(r'^delete_weapon/(?P<weapon_id>\d+)/$$', 'weapon.views.delete_weapon', name ='delete_weapon'),
    )
