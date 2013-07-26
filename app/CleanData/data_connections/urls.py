from django.conf.urls.defaults import *

urlpatterns = patterns('data_connections.views',
    url(r'^$', 'index',name='index'),
    (r'^add_dataset','add_dataset'),
)