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

urlpatterns += patterns('contcombapi.vehicle.views',
    url(r'^vehicle/get/user$', 'get_by_user'),
    url(r'^vehicle/save$', 'save'),
    url(r'^vehicle/update$', 'update'),
    url(r'^vehicle/get/(?P<id_car>[^/]+)$', 'get_by_id'),
    url(r'^vehicle/delete/(?P<id_car>[^/]+)$', 'delete'),
    url(r'^vehicle/get_models$', 'get_models'),
    url(r'^vehicle/fuel/get/user$', 'get_vehicle_fuel_by_user'),
    url(r'^vehicle/ranking$', 'get_ranking'),
)

urlpatterns += patterns('contcombapi.supply.views',
    url(r'^supply/get/user/(?P<id_vehicle>[^/]+)$', 'get_by_user_vehicle'),
    url(r'^supply/save$', 'save'),
    url(r'^supply/update$', 'update'),
    url(r'^supply/get/(?P<id_supply>[^/]+)$', 'get_by_id'),
    url(r'^supply/delete/(?P<id_supply>[^/]+)$', 'delete'),
    url(r'^supply/get/summary/(?P<id_vehicle>[^/]+)$', 'get_summary_by_vehicle'),
    url(r'^supply/import/old$', 'import_old_contcomb'),
    
)