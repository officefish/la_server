from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from card import urls as card_urls
from hero import  urls as hero_urls
from api import urls as api_urls
from book import urls as book_urls
from bookMask import urls as book_mask_urls
from group import  urls as group_urls
from achieve import urls as achieve_urls

urlpatterns = patterns('',

    url(r'^cards/', include(card_urls), name='cards'),
    url(r'^heroes/', include(hero_urls), name='heroes'),
    url(r'^books/', include(book_urls), name='books'),
    url(r'^mask/', include(book_mask_urls), name='mask'),
    url(r'^api/', include(api_urls), name='api'),
    url(r'^groups/', include(group_urls), name='group'),
    url(r'^achieves/',include(achieve_urls),name='achieve'),
    # Examples:
    # url(r'^$', 'last_argument.views.home', name='home'),
    # url(r'^last_argument/', include('last_argument.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
