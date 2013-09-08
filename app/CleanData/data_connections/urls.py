from django.conf.urls.defaults import *
from tastypie.api import Api
from data_connections.api import *

v1_api = Api(api_name='v1')
v1_api.register(ScientistResource())
v1_api.register(LicenseResource())
v1_api.register(FormatResource())
v1_api.register(OrganizationResource())
v1_api.register(DatasetResource())
v1_api.register(DatasetSourcesResource())
v1_api.register(DatasetDerivativesResource())
v1_api.register(DataRelationResource())
v1_api.register(MinimalDatasetResource())
v1_api.register(DatasetUrlResource())

urlpatterns = patterns('data_connections.views',
    url(r'^$', 'dataset_view',name='index'),
	url(r'^dataset/(?P<dataset_id>\d+)', 'dataset_view',name="dataset_detail"),
	url(r'^license/(?P<license_id>\d+)', 'license_view',name="license_detail"),
	url(r'^data_format/(?P<format_id>\d+)', 'format_view',name="format_detail"),
	url(r'^all_datasets','all_datasets',name="all_datasets"),
	url(r'^scientist/(?P<scientist_id>\d+)', 'scientist_view',name="scientist_detail"),
	url(r'^data_catalog/(?P<data_catalog_id>\d+)', 'catalog_view',name="data_catalog_detail"),
	url(r'^organization/(?P<organization_id>\d+)', 'organization_view',name="organization_detail"),
	# the add/edit/delete views
    (r'^add_dataset','add_dataset'),
    (r'^add_application','add_application'),
    (r'^add_datarelation','add_datarelation'),
    (r'^search','search'),
    (r'^api/', include(v1_api.urls)),
)