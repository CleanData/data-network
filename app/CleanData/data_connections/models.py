from django.db import models
from django.contrib.auth.models import User

# The data models
class DataCatalog(models.Model):
	name = models.CharField(max_length=200)
	manager = models.ForeignKey("UserProfile",related_name="managed_datacatalogs")
	managing_organization = models.ForeignKey("Organization",related_name="managed_datacatalogs",null=True,blank=True)
	
	def __unicode__(self):
		return self.name

class License(models.Model):
	name = models.CharField(max_length=200)
	url = models.URLField(blank=True)
	def __unicode__(self):
		return self.name

class Format(models.Model):
	name = models.CharField(max_length=200)
	url = models.URLField(blank=True)
	def __unicode__(self):
		return self.name
	
class Dataset(models.Model):
	data_catalog = models.ForeignKey(DataCatalog,null=True,blank=True)
	name = models.CharField(max_length=200)
	date_published = models.DateTimeField('date published')
	date_last_edited = models.DateTimeField('date last edited')
	url = models.URLField(blank=True)
	# relationships
	data_format = models.ForeignKey(Format,related_name="formatted_datasets",null=True,blank=True)
	license = models.ForeignKey(License,related_name="licensed_datasets",null=True,blank=True)
	sources = models.ManyToManyField('self', through='DataRelation', symmetrical=False,
									related_name='derivatives',null=True,blank=True)
	contributors = models.ManyToManyField('UserProfile', through='ContributorRelation', symmetrical=False,
									related_name='contributed_datasets',null=True,blank=True)
	manager = models.ForeignKey("UserProfile",related_name="managed_datasets",null=True,blank=True)
	managing_organization = models.ForeignKey("Organization",related_name="managed_datasets",null=True,blank=True)

	#def url_string(self):
	#	# return name+date
	
	def __unicode__(self):
		return self.name

class DataRelation(models.Model):
	source = models.ForeignKey(Dataset, related_name='relation_to_derivative')
	derivative = models.ForeignKey(Dataset, related_name='relation_to_source')
	how_data_was_processed = models.TextField(max_length=20000)

	def __unicode__(self):
		return self.source.name+" -> "+self.derivative.name


# The membership/organisation models
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	collaborators = models.ManyToManyField('self')
	def __unicode__(self):
		return self.user.name
	
class Organization(models.Model):
	name = models.CharField(max_length=200)
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
	work_done = models.TextField(max_length=20000)
	
	def __unicode__(self):
		return self.contributor.name+" -> "+self.dataset.name	
	
	
	
	
	
	
	
	
