# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
   url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('contcombapi.authentication.views',
    url(r'^generate_token/$', 'generate_token'),
)

urlpatterns += patterns('contcombapi.user.views',
    url(r'^user/get/all/$', 'get_all'),
    url(r'^user/get/(?P<id_user>[^/]+)/$', 'get_by_pk'),
    url(r'^user/get/username/(?P<username>[^/]+)$', 'get_by_username'),
    url(r'^user/save$', 'save'),
    url(r'^user/update$', 'update'),
    url(r'^user/delete/(?P<id_user>[^/]+)/$', 'delete'),
)


urlpatterns += patterns('contcombapi.contact.views',
    url(r'^contact/save$', 'save'),
    url(r'^contact/get/user$', 'get_by_user'),
    url(r'^contact/get/(?P<id_message>[^/]+)$', 'get_by_id'),
    url(r'^contact/delete/(?P<id_message>[^/]+)$', 'delete'),
)
