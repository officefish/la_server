__author__ = 'inozemcev'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'achieve.views.achieve_list',
                           name='achieves_list'),
                       url(r'create/$', 'achieve.views.create_achieve',
                           name='create_achieve'),
                       url(r'edit_achieve/(?P<achieve_id>\d+)/$',
                           'achieve.views.edit_achieve', name='edit_achieve'),
                       url(r'delete_achieve/(?P<achieve_id>\d+)/$',
                           'achieve.views.delete_achieve', name='delete_achieve'),
                       url(r'^add_achieve_owner/(?P<achieve_id>\d+)/$',
                           'achieve.views.add_achieve_owner', name='add_achieve_owner'),
                       url(r'^remove_achieve_owner/(?P<achieve_id>\d+)/(?P<hero_id>\d+)/$',
                           'achieve.views.remove_achieve_owner', name='remove_achieve_owner'),
                       url(r'achieve_masks/$', 'achieve.views.mask_list',
                           name='achieve_masks'),
                       url(r'edit_achieve_mask/(?P<mask_id>\d+)/$',
                           'achieve.views.edit_achieve_mask', name='edit_achieve_mask')

                       )
