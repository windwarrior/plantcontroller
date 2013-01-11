from django.conf.urls import patterns, include, url
from jsonrpc import jsonrpc_site

import views

from plantcontroller import api

urlpatterns = patterns('',
	url(r'^$', 'plantcontroller.views.monitor'),
    url(r'^api/browse/$', 'jsonrpc.views.browse', name='jsonrpc_browser'),
    url(r'^api/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
)
