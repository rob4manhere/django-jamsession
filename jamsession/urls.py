from django.conf.urls.defaults import *

from jamsession.views.admin import (dashboard, create_object, edit_object)

urlpatterns = patterns('',
    url(r'^admin/$', dashboard, name="admin-dashboard"),
    url(r'^admin/(?P<object_type>\w+)/add/$', create_object, name='admin-create-object'),
    url(r'^admin/(?P<object_type>\w+)/edit/(?P<object_id>(.*?))/$', edit_object, name='admin-edit-object'),
)
