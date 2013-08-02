from django.conf.urls.defaults import *
from tastypie.api import Api
from data_connections.api import DatasetResource, ScientistResource, DataRelationResource

v1_api = Api(api_name='v1')
v1_api.register(ScientistResource())
v1_api.register(DatasetResource())
v1_api.register(DataRelationResource())

urlpatterns = patterns('data_connections.views',
    url(r'^$', 'index',name='index'),
    url(r'^tree', 'tree_view',name='tree_view'),
    (r'^add_dataset','add_dataset'),
    (r'^api/', include(v1_api.urls)),
)