from tastypie import fields
from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS
from data_connections.models import *
from django.contrib.auth.models import User
from tastypie.authentication import Authentication
from tastypie.cache import SimpleCache

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        detail_uri_name = 'username'

class ScientistResource(ModelResource):
	class Meta:
		queryset = Scientist.objects.all()
		resource_name = 'scientist'		
		allowed_methods = ['get']
		authentication = Authentication()
		cache=SimpleCache()
		filtering = {
			'firstname':ALL,
		}
class LicenseResource(ModelResource):
	class Meta:
		queryset = License.objects.all()
		resource_name = 'license'		
		allowed_methods = ['get']
		authentication = Authentication()
		cache=SimpleCache()
class FormatResource(ModelResource):
	class Meta:
		queryset = Format.objects.all()
		resource_name = 'format'		
		allowed_methods = ['get']
		authentication = Authentication()
		cache=SimpleCache()
class OrganizationResource(ModelResource):
	class Meta:
		queryset = Organization.objects.all()
		resource_name = 'organization'		
		allowed_methods = ['get']
		authentication = Authentication()
		cache=SimpleCache()
class DataCatalogResource(ModelResource):
	class Meta:
		queryset = DataCatalog.objects.all()
		resource_name = 'data_catalog'		
		allowed_methods = ['get']
		authentication = Authentication()
		cache=SimpleCache()
class DistributionResource(ModelResource):
	data_format = fields.ForeignKey(FormatResource, 'data_format',full=True)
	license = fields.ForeignKey(LicenseResource, 'license',full=True)
	class Meta:
		queryset = Distribution.objects.all()
		resource_name = 'distribution'		
		allowed_methods = ['get']
		authentication = Authentication()
		cache=SimpleCache()
class DataRelationResource(ModelResource):
	source = fields.ToOneField('data_connections.api.DatasetResource', 'source',full=True)
	derivative = fields.ToOneField('data_connections.api.DatasetResource', 'derivative',full=True)
	class Meta:
		queryset = DataRelation.objects.all()
		resource_name = 'datarelation'
		allowed_methods = ['get']
        authentication = Authentication()
        cache=SimpleCache()
		
class DatasetResource(ModelResource):
	# note that the name in the ForeignKey relation here is the name of the foreign key field we're mapping to.
	scientist = fields.ForeignKey(ScientistResource, 'manager',null=True,blank=True)
	organization = fields.ForeignKey(OrganizationResource, 'managing_organization',null=True,blank=True,full=True)
	sources = fields.ToManyField('self','derivatives')
	derivatives = fields.ToManyField('self','sources') 	
	class Meta:
		queryset = Dataset.objects.all()
		resource_name = 'dataset'
		allowed_methods = ['get']
		authentication = Authentication()
		cache=SimpleCache()
		filtering = {
			'title': ALL,
			'data_format': ALL,
			'landingPage': ALL,
		}
        
class DatasetDerivativesResource(ModelResource):
	# note that the name in the ForeignKey relation here is the name of the foreign key field we're mapping to.
	contactPoint = fields.ForeignKey(ScientistResource,'contactPoint',null=True,blank=True,full=True)
	organization = fields.ForeignKey(OrganizationResource, 'managing_organization',null=True,blank=True,full=True)
	#license = fields.ForeignKey(LicenseResource, 'license',full=True)
	added_by = fields.ForeignKey(UserResource, 'added_by',full=False, null=True, blank=True)
	#data_format = fields.ForeignKey(FormatResource, 'data_format',full=True)
	data_catalog = fields.ForeignKey(DataCatalogResource, 'data_catalog',null=True,blank=True,full=True)
	
	distributions = fields.ToManyField(DistributionResource,'distributions',full=True)
	
	children = fields.ToManyField('self',
				'derivatives',
				full=True)
	class Meta:
		queryset = Dataset.objects.all()
		resource_name = 'dataset_derivatives'
		allowed_methods = ['get']
		authentication = Authentication()
		cache=SimpleCache()
		filtering = {
			'title': ALL,
			'data_format': ALL,
			'accessors': ALL,
			'is_public': ALL,
			'added_by': ALL,			
		}
        
class DatasetSourcesResource(ModelResource):
	# note that the name in the ForeignKey relation here is the name of the foreign key field we're mapping to.
	contactPoint = fields.ForeignKey(ScientistResource, 'contactPoint',null=True,blank=True,full=True)
	#license = fields.ForeignKey(LicenseResource, 'license',full=True)
	added_by = fields.ForeignKey(UserResource, 'added_by',full=False, null=True, blank=True)
	#data_format = fields.ForeignKey(FormatResource, 'data_format',full=True)

	data_catalog = fields.ForeignKey(DataCatalogResource, 'data_catalog',null=True,blank=True,full=True)
	organization = fields.ForeignKey(OrganizationResource, 'managing_organization',null=True,blank=True,full=True)
	
	distributions = fields.ToManyField(DistributionResource,'distributions',full=True)
	
	#sources = fields.ToManyField('self','derivatives')
	children = fields.ToManyField('self','sources',full=True)
	class Meta:
		queryset = Dataset.objects.all()
		resource_name = 'dataset_sources'
		allowed_methods = ['get']
		authentication = Authentication()
		cache=SimpleCache()
		filtering = {
			'title': ALL,
			'data_format': ALL,
			'accessors': ALL,
			'is_public': ALL,
			'added_by': ALL,
		}
        
class MinimalDatasetResource(ModelResource):
	data_format = fields.ForeignKey(FormatResource, 'data_format',full=True)
	class Meta:
		queryset = Dataset.objects.all()
		resource_name = 'min_dataset'
		allowed_methods = ['get']
		authentication = Authentication()
		cache=SimpleCache()
		filtering = {
			'title': ALL,
			'landingPage': ALL,
		}

class DatasetUrlResource(ModelResource):
	class Meta:
		queryset = Dataset.objects.all()
		fields = ['landingPage']
		resource_name = 'dataset_url'
		allowed_methods = ['get']
		authentication = Authentication()
		cache=SimpleCache()
		filtering = {
			'landingPage': ALL
		}


""""
# the test version which includes the -through- data.
sources = fields.ToManyField(DataRelationResource,
						attribute=lambda bundle: bundle.obj.sources.through.objects.filter(
						recipe=bundle.obj) or bundle.obj.ingredients, full=True)

ingredients = fields.ToManyField(RecipeIngredientResource,
        attribute=lambda bundle: bundle.obj.ingredients.through.objects.filter(
            recipe=bundle.obj) or bundle.obj.ingredients, full=True)
	"""


