from django.conf.urls import patterns, include, url
from jsonrpc import jsonrpc_site

import views

from plantcontroller import jsonrpc_methods, post_methods

urlpatterns = patterns('',
	url(r'^$', 'plantcontroller.views.monitor'),
    url(r'^login/$', 'plantcontroller.views.login_wrapper'), 
    url(r'^jsonapi/browse/$', 'jsonrpc.views.browse', name='jsonrpc_browser'),
    url(r'^jsonapi/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
    url(r'^api/add/$', 'plantcontroller.post_methods.add_data_point'),
)
