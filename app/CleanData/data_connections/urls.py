from django.conf.urls.defaults import *
from tastypie.api import Api
from data_connections.api import *

# This needs to disappear in the production version.
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
    url(r'^source_deriv_tree/(?P<dataset_id>\d+)','getDerivsAndSources',name='source_deriv_tree'),
	url(r'^dataset/random$', 'random_dataset_view',name="random_dataset"),
	url(r'^dataset/(?P<dataset_id>\d+)', 'dataset_view',name="dataset_detail"),
	url(r'^license/(?P<license_id>\d+)', 'license_view',name="license_detail"),
	url(r'^data_format/(?P<format_id>\d+)', 'format_view',name="format_detail"),
	url(r'^all_datasets$','all_datasets',name="all_datasets"),
	url(r'^scientist/(?P<scientist_id>\d+)', 'scientist_view',name="scientist_detail"),
	url(r'^data_catalog/(?P<data_catalog_id>\d+)', 'catalog_view',name="data_catalog_detail"),
	url(r'^organization/(?P<organization_id>\d+)', 'organization_view',name="organization_detail"),
	# the add/edit/delete views
    url(r'^add_dataset$','add_dataset',name="add_dataset"),
    url(r'^edit/(?P<dataset_id>\d+)','edit_dataset',name='edit_dataset'),
    url(r'^delete/(?P<dataset_id>\d+)','delete_dataset',name='delete_dataset'),
    url(r'^add_application$','add_application',name="add_application"),
    url(r'^add_datarelation$','add_datarelation',name="add_datarelation"),
    url(r'^search$','search'),
    url(r'^searchAPI$','searchAPI'),
	# toggle this to check the underlying API is working
    #(r'^api/', include(v1_api.urls)),
)