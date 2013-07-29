from django.db import models
from django.contrib.auth.models import User

# The data models
class DataCatalogManager(models.Manager):
	def get_by_natural_key(self,name):
		return self.get(name=name)
class DataCatalog(models.Model):
	objects = DataCatalogManager()	# handles natural keys

	name = models.CharField(max_length=200, unique=True)
	manager = models.ForeignKey("UserProfile",related_name="managed_datacatalogs")
	managing_organization = models.ForeignKey("Organization",related_name="managed_datacatalogs",null=True,blank=True)
	
	def __unicode__(self):
		return self.name

class LicenseManager(models.Manager):
	def get_by_natural_key(self,name):
		return self.get(name=name)
class License(models.Model):
	objects = LicenseManager() 		# handles natural keys

	name = models.CharField(max_length=200,unique=True)
	url = models.URLField(blank=True)
	def __unicode__(self):
		return self.name

class FormatManager(models.Manager):
	def get_by_natural_key(self,name):
		return self.get(name=name)
class Format(models.Model):
	objects = FormatManager() 		# handles natural keys

	name = models.CharField(max_length=200, unique=True)
	url = models.URLField(blank=True)
	def __unicode__(self):
		return self.name

# sorts out natural identification of datasets
class DatasetManager(models.Manager):
	def get_by_natural_key(self,url,name):
		return self.get(url=url,name=name)
class Dataset(models.Model):
	objects = DatasetManager()		# handles natural keys
	
	data_catalog = models.ForeignKey(DataCatalog,null=True,blank=True)
	name = models.CharField(max_length=100)
	date_published = models.DateTimeField('date published')
	date_last_edited = models.DateTimeField('date last edited')
	url = models.URLField(max_length=150)
	description = models.TextField(blank=True)

	#added_by = models.CharField(max_length=200,blank=True,)

	# relationships
	data_format = models.ForeignKey(Format,related_name="formatted_datasets",null=True,blank=True)
	license = models.ForeignKey(License,related_name="licensed_datasets",null=True,blank=True)
	sources = models.ManyToManyField('self', through='DataRelation', symmetrical=False,
									related_name='derivatives',null=True,blank=True)
	contributors = models.ManyToManyField('UserProfile', through='ContributorRelation', symmetrical=False,
									related_name='contributed_datasets',null=True,blank=True)
	# scientists who are identified as managers, but who are not registered users of Clean.Data.
	unreg_manager = models.ForeignKey("UnregScientist",related_name="managed_datasets",null=True,blank=True)
	# scientists who are identified as managers, and who are registered users of Clean.Data.
	manager = models.ForeignKey("UserProfile",related_name="managed_datasets",null=True,blank=True)
	managing_organization = models.ForeignKey("Organization",related_name="managed_datasets",null=True,blank=True)

	def __unicode__(self):
		return self.name
	class Meta:
		unique_together = (('name','url'),)


class DataRelation(models.Model):
	source = models.ForeignKey(Dataset, related_name='relation_to_derivative')
	derivative = models.ForeignKey(Dataset, related_name='relation_to_source')
	how_data_was_processed = models.TextField(max_length=20000,blank=True)

	def __unicode__(self):
		return self.source.name+" -> "+self.derivative.name


# The membership/organisation models

# This is a class to store a reference to a datascientist that's not registered as a user of the site
# This will be most of the scientists.
# Note that the natural key is first, last, and profile url. This should keep things more or less unique.
class UnregScientistManager(models.Manager):
	def get_by_natural_key(self,firstname,lastname,profile_url):
		return self.get(firstname=firstname,lastname=lastname,profile_url=profile_url)
class UnregScientist(models.Model):
	objects = UnregScientistManager()		# handles natural keys
	
	firstname = models.CharField(max_length=30)
	lastname = models.CharField(max_length=30,blank=True)
	profile_url = models.URLField(max_length=150,blank=True,default="")
	class Meta:
		unique_together = (("firstname","lastname","profile_url"),)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	collaborators = models.ManyToManyField('self')
	def __unicode__(self):
		return self.user.name
	
class OrganizationManager(models.Manager):
	def get_by_natural_key(self,name):
		return self.get(name=name)
class Organization(models.Model):
	objects = OrganizationManager()		# handles natural keys

	name = models.CharField(max_length=200,unique=True)
	url = models.URLField(max_length=150,default="")
	def __unicode__(self):
		return self.name

class MembershipRelation(models.Model):
	organization = models.ForeignKey(Organization, related_name='relation_to_member')
	member = models.ForeignKey(UserProfile, related_name='relation_to_organization')

	def __unicode__(self):
		return self.member.name+" -> "+self.organization.name
	
class ContributorRelation(models.Model):
	contributor = models.ForeignKey(UserProfile, related_name='relation_to_data')
	dataset = models.ForeignKey(Dataset, related_name='relation_to_contributor')
	work_done = models.TextField(max_length=20000, blank=True)
	
	def __unicode__(self):
		return self.contributor.name+" -> "+self.dataset.name	
	
	
	
	
	
	
	
	
