from django.conf.urls.defaults import *

urlpatterns = patterns('data_connections.views',
    (r'^$', 'index'),
)