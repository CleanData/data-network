from tastypie import fields
from tastypie.resources import Resource, ModelResource
from data_connections.models import Dataset, Scientist, DataRelation
from tastypie.authentication import Authentication
from tastypie.cache import SimpleCache



class ScientistResource(ModelResource):
	class Meta:
		queryset = Scientist.objects.all()
		resource_name = 'scientist'		
		allowed_methods = ['get']
        authentication = Authentication()
        cache=SimpleCache()
	
class DataRelationResource(ModelResource):
	source = fields.ToOneField('data_connections.api.DatasetResource', 'source',full=True)
	derivative = fields.ToOneField('data_connections.api.DatasetResource', 'derivative',full=True)
	class Meta:
		queryset = DataRelation.objects.all()
		resource_name = 'datarelation'
		
class DatasetResource(ModelResource):
	# note that the name in the ForeignKey relation here is the name of the foreign key field we're mapping to.
	scientist = fields.ForeignKey(ScientistResource, 'unreg_manager',null=True,blank=True)
	
	sources = fields.ToManyField('self','derivatives')
	derivatives = fields.ToManyField('self','sources')
	
	""""
	# the test version which includes the -through- data.
	sources = fields.ToManyField(DataRelationResource,
							attribute=lambda bundle: bundle.obj.sources.through.objects.filter(
							recipe=bundle.obj) or bundle.obj.ingredients, full=True)

    ingredients = fields.ToManyField(RecipeIngredientResource,
            attribute=lambda bundle: bundle.obj.ingredients.through.objects.filter(
                recipe=bundle.obj) or bundle.obj.ingredients, full=True)
 	"""
 	
	class Meta:
		queryset = Dataset.objects.all()
		resource_name = 'dataset'
		allowed_methods = ['get']
		authentication = Authentication()
        cache=SimpleCache()

