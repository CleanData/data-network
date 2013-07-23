from django.conf.urls.defaults import *

urlpatterns = patterns('data_connections.views',
    url(r'^$', 'index',name='index'),
    (r'^dataset','add_dataset'),
)