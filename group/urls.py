__author__ = 'RIK'
__author__ = 'inozemcev'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
      url(r'^create_group/(?P<card_id>\d+)/$', 'group.views.create_group', name='create_group'),
    )