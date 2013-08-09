from django.conf.urls.defaults import *
from tastypie.api import Api
from data_connections.api import *

v1_api = Api(api_name='v1')
v1_api.register(ScientistResource())
v1_api.register(LicenseResource())
v1_api.register(FormatResource())
v1_api.register(DatasetResource())
v1_api.register(DatasetSourcesResource())
v1_api.register(DatasetDerivativesResource())
v1_api.register(DataRelationResource())

urlpatterns = patterns('data_connections.views',
    url(r'^$', 'tree_view',name='index'),
	url(r'^license/(?P<license_id>\d+)', 'license_view'),
	url(r'^data_format/(?P<format_id>\d+)', 'format_view'),
	url(r'^scientist/(?P<scientist_id>\d+)', 'scientist_view'),
    (r'^add_dataset','add_dataset'),
    (r'^api/', include(v1_api.urls)),
)