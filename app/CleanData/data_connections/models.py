from django.db import models
from django.contrib.auth.models import User

"""
class DataCatalog(models.Model):
	objects = DataCatalogManager()	# handles natural keys

	name = models.CharField(max_length=200, unique=True)
	manager = models.ForeignKey("Scientist",related_name="managed_datacatalogs",null=True,blank=True)
	managing_organization = models.ForeignKey("Organization",related_name="managed_datacatalogs",null=True,blank=True)
	
	def __unicode__(self):
		return self.name
"""

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

class KeywordManager(models.Manager):
	def get_by_natural_key(self,keyword):
		return self.get(keyword=keyword)
class Keyword(models.Model):
	keyword = models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return self.keyword

class CategoryManager(models.Manager):
	def get_by_natural_key(self,category):
		return self.get(category=category)
class Category(models.Model):
	category = models.CharField(max_length=100, unique=True)
	def __unicode__(self):
		return self.category

# The data models
class DataCatalogManager(models.Manager):
	def get_by_natural_key(self,title):
		return self.get(title=title)
class DataCatalog(models.Model):
	objects = DataCatalogManager()		# handles natural keys

	title = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)

	issued = models.DateTimeField('date published')
	modified = models.DateTimeField('date last edited')

	language = models.CharField(max_length=3, default="en")
	license = models.ForeignKey(License,related_name="licensed_datacatalogs",null=True,blank=True)
	homepage = models.URLField(max_length=200,blank=True)

	spatial = models.CharField( max_length=500, default="",
								name="Geographic region of the dataset (if applicable)",
								null=True,blank=True)

	manager = models.ForeignKey("Scientist",related_name="managed_datacatalogs",null=True,blank=True)
	managing_organization = models.ForeignKey("Organization",related_name="managed_datacatalogs",null=True,blank=True)
	

	categories = models.ManyToManyField(Category, related_name='catalogs',
										null=True, blank=True)
	keywords = models.ManyToManyField(Keyword, related_name='catalogs',
										null=True, blank=True)
	
	def __unicode__(self):
		return self.title


"""
class Dataset(models.Model):
	objects = DatasetManager()		# handles natural keys
	
	data_catalog = models.ForeignKey(DataCatalog,null=True,blank=True)
	# sets the registered user who added the dataset
	added_by = models.ForeignKey(User,null=True,blank=True)

	name = models.CharField(max_length=200)
	date_published = models.DateTimeField('date published')
	date_last_edited = models.DateTimeField('date last edited')
	url = models.URLField(max_length=200)
	documentation_url = models.URLField(max_length=200,blank=True)
	download_url = models.URLField(max_length=200,blank=True)
	description = models.TextField(blank=True)

	# relationships
	data_format = models.ForeignKey(Format,related_name="formatted_datasets",null=True,blank=True)
	license = models.ForeignKey(License,related_name="licensed_datasets",null=True,blank=True)
	derivatives = models.ManyToManyField('self', through='DataRelation', symmetrical=False,
									related_name='sources',null=True,blank=True)
	#sources = models.ManyToManyField('self', through='DataRelation', symmetrical=False,
	#								related_name='derivatives',null=True,blank=True)
	contributors = models.ManyToManyField('Scientist', through='ContributorRelation', symmetrical=False,
									related_name='contributed_datasets',null=True,blank=True)

	manager = models.ForeignKey("Scientist",related_name="managed_datasets",null=True,blank=True)

	# scientists who are identified as managers, and who are registered users of Clean.Data.
	managing_organization = models.ForeignKey("Organization",related_name="managed_datasets",null=True,blank=True)

	is_public = models.BooleanField(verbose_name="Is this visible to others?", default = True)

	def __unicode__(self):
		return self.name
	#class Meta:
	#	unique_together = (('name','url'),)
"""
class DatasetManager(models.Manager):
	def get_by_natural_key(self,title):
		return self.get(title=title)

class Dataset(models.Model):
	objects = DatasetManager()		# handles natural keys

	data_catalog = models.ForeignKey(DataCatalog,null=True,blank=True)
	# sets the registered user who added the dataset
	added_by = models.ForeignKey(User,null=True,blank=True)

	title = models.CharField(max_length=300)
	description = models.TextField(blank=True)

	issued = models.DateTimeField('date published')
	modified = models.DateTimeField('date last edited')
	
	LANGUAGES = (
	('en','English'),
	('ab','Abkhaz'),
	('aa','Afar'),
	('af','Afrikaans'),
	('ak','Akan'),
	('sq','Albanian'),
	('am','Amharic'),
	('ar','Arabic'),
	('an','Aragonese'),
	('hy','Armenian'),
	('as','Assamese'),
	('av','Avaric'),
	('ae','Avestan'),
	('ay','Aymara'),
	('az','Azerbaijani'),
	('bm','Bambara'),
	('ba','Bashkir'),
	('eu','Basque'),
	('be','Belarusian'),
	('bn','Bengali'),
	('bh','Bihari'),
	('bi','Bislama'),
	('bs','Bosnian'),
	('br','Breton'),
	('bg','Bulgarian'),
	('my','Burmese'),
	('ca','Catalan; Valencian'),
	('ch','Chamorro'),
	('ce','Chechen'),
	('ny','Chichewa; Chewa; Nyanja'),
	('zh','Chinese'),
	('cv','Chuvash'),
	('kw','Cornish'),
	('co','Corsican'),
	('cr','Cree'),
	('hr','Croatian'),
	('cs','Czech'),
	('da','Danish'),
	('dv','Divehi; Dhivehi; Maldivian;'),
	('nl','Dutch'),
	('eo','Esperanto'),
	('et','Estonian'),
	('ee','Ewe'),
	('fo','Faroese'),
	('fj','Fijian'),
	('fi','Finnish'),
	('fr','French'),
	('ff','Fula; Fulah; Pulaar; Pular'),
	('gl','Galician'),
	('ka','Georgian'),
	('de','German'),
	('el','Greek, Modern'),
	('gn','Guarani'),
	('gu','Gujarati'),
	('ht','Haitian; Haitian Creole'),
	('ha','Hausa'),
	('he','Hebrew (modern)'),
	('hz','Herero'),
	('hi','Hindi'),
	('ho','Hiri Motu'),
	('hu','Hungarian'),
	('ia','Interlingua'),
	('id','Indonesian'),
	('ie','Interlingue'),
	('ga','Irish'),
	('ig','Igbo'),
	('ik','Inupiaq'),
	('io','Ido'),
	('is','Icelandic'),
	('it','Italian'),
	('iu','Inuktitut'),
	('ja','Japanese'),
	('jv','Javanese'),
	('kl','Kalaallisut, Greenlandic'),
	('kn','Kannada'),
	('kr','Kanuri'),
	('ks','Kashmiri'),
	('kk','Kazakh'),
	('km','Khmer'),
	('ki','Kikuyu, Gikuyu'),
	('rw','Kinyarwanda'),
	('ky','Kirghiz, Kyrgyz'),
	('kv','Komi'),
	('kg','Kongo'),
	('ko','Korean'),
	('ku','Kurdish'),
	('kj','Kwanyama, Kuanyama'),
	('la','Latin'),
	('lb','Luxembourgish, Letzeburgesch'),
	('lg','Luganda'),
	('li','Limburgish, Limburgan, Limburger'),
	('ln','Lingala'),
	('lo','Lao'),
	('lt','Lithuanian'),
	('lu','Luba-Katanga'),
	('lv','Latvian'),
	('gv','Manx'),
	('mk','Macedonian'),
	('mg','Malagasy'),
	('ms','Malay'),
	('ml','Malayalam'),
	('mt','Maltese'),
	('mi','Maori'),
	('mr','Marathi'),
	('mh','Marshallese'),
	('mn','Mongolian'),
	('na','Nauru'),
	('nv','Navajo, Navaho'),
	('nb','Norwegian Bokmal'),
	('nd','North Ndebele'),
	('ne','Nepali'),
	('ng','Ndonga'),
	('nn','Norwegian Nynorsk'),
	('no','Norwegian'),
	('ii','Nuosu'),
	('nr','South Ndebele'),
	('oc','Occitan'),
	('oj','Ojibwe, Ojibwa'),
	('cu','Old Church Slavonic, Church Slavic, Church Slavonic, Old Bulgarian, Old Slavonic'),
	('om','Oromo'),
	('or','Oriya'),
	('os','Ossetian, Ossetic'),
	('pa','Panjabi, Punjabi'),
	('pi','Pali'),
	('fa','Persian'),
	('pl','Polish'),
	('ps','Pashto, Pushto'),
	('pt','Portuguese'),
	('qu','Quechua'),
	('rm','Romansh'),
	('rn','Kirundi'),
	('ro','Romanian, Moldavian, Moldovan'),
	('ru','Russian'),
	('sa','Sanskrit'),
	('sc','Sardinian'),
	('sd','Sindhi'),
	('se','Northern Sami'),
	('sm','Samoan'),
	('sg','Sango'),
	('sr','Serbian'),
	('gd','Scottish Gaelic; Gaelic'),
	('sn','Shona'),
	('si','Sinhala, Sinhalese'),
	('sk','Slovak'),
	('sl','Slovene'),
	('so','Somali'),
	('st','Southern Sotho'),
	('es','Spanish; Castilian'),
	('su','Sundanese'),
	('sw','Swahili'),
	('ss','Swati'),
	('sv','Swedish'),
	('ta','Tamil'),
	('te','Telugu'),
	('tg','Tajik'),
	('th','Thai'),
	('ti','Tigrinya'),
	('bo','Tibetan Standard, Tibetan, Central'),
	('tk','Turkmen'),
	('tl','Tagalog'),
	('tn','Tswana'),
	('to','Tonga (Tonga Islands)'),
	('tr','Turkish'),
	('ts','Tsonga'),
	('tt','Tatar'),
	('tw','Twi'),
	('ty','Tahitian'),
	('ug','Uighur, Uyghur'),
	('uk','Ukrainian'),
	('ur','Urdu'),
	('uz','Uzbek'),
	('ve','Venda'),
	('vi','Vietnamese'),
	('vo','Volapuk'),
	('wa','Walloon'),
	('cy','Welsh'),
	('wo','Wolof'),
	('fy','Western Frisian'),
	('xh','Xhosa'),
	('yi','Yiddish'),
	('yo','Yoruba'),
	('za','Zhuang, Chuang')
	)
	language = models.CharField(max_length=2, verbose_name="Primary language", choices = LANGUAGES, default="en")
	landingPage = models.URLField(max_length=200)

	contactPoint = models.ForeignKey("Scientist",related_name="managed_datasets",null=True,blank=True)
	#manager = models.ForeignKey("Scientist",related_name="managed_datasets",null=True,blank=True)

	temporalStart = models.DateTimeField(verbose_name='Start date of dataset (if applicable)',null=True,blank=True,default=None)
	temporalEnd = models.DateTimeField(verbose_name='End date of dataset (if applicable)',null=True,blank=True,default=None)

	spatial = models.CharField(max_length=500, default="", verbose_name="Geographic region of the dataset (if applicable)",null=True,blank=True)
	
	ACCRUAL_CHOICES = (
	    ('NO', 'doesn\'t accrue'),
	    ('AN', 'as needed'),
	    ('IN', 'intermittent'),
	    ('RT', 'real time'),
	    ('MI', 'every minute'),
	    ('HO', 'hourly'),
	    ('DA', 'daily'),
	    ('WE', 'weekly'),
	    ('BW', 'biweekly'),
	    ('MO', 'monthly'),
	    ('BM', 'bimonthly'),
	    ('QU', 'quarterly'),
	    ('YE', 'yearly'),
	    ('BY', 'biyearly'),
	    ('DE', 'decadal'),
	    ('OT', 'other'),
	)	
	accrualPeriodicity = models.CharField(  max_length=2, 
											choices = ACCRUAL_CHOICES,
											default='NO',
											name="Accrual period")

	derivatives = models.ManyToManyField('self', through='DataRelation', symmetrical=False,
									related_name='sources',null=True,blank=True)
	#sources = models.ManyToManyField('self', through='DataRelation', symmetrical=False,
	#								related_name='derivatives',null=True,blank=True)
	contributors = models.ManyToManyField('Scientist', through='ContributorRelation', symmetrical=False,
									related_name='contributed_datasets',null=True,blank=True)

	# scientists who are identified as managers, and who are registered users of Clean.Data.
	managing_organization = models.ForeignKey("Organization",related_name="managed_datasets",null=True,blank=True)

	categories = models.ManyToManyField(Category, related_name='datasets',
										null=True, blank=True)
	keywords = models.ManyToManyField(Keyword, related_name='datasets',
										null=True, blank=True)

	is_public = models.BooleanField(verbose_name="Is this visible to others?", default = True)

	def __unicode__(self):
		return self.title
	#class Meta:
	#	unique_together = (('name','url'),)

# sorts out natural identification of datasets
class DistributionManager(models.Manager):
	def get_by_natural_key(self,dataset,data_format):
		return self.get(dataset=dataset,data_format=data_format)
class Distribution(models.Model):
	objects = DistributionManager()		# handles natural keys

	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)

	issued = models.DateTimeField('date published')
	modified = models.DateTimeField('date last edited')

	license = models.ForeignKey(License,related_name="licensed_datasets",null=True,blank=True)

	# these are charfields rather than urls as we might have a filepath here instead for local files
	accessURL = models.CharField(max_length=300,blank=True, verbose_name="access location")
	downloadURL = models.CharField(max_length=300,blank=True, verbose_name = "file location")

	dataset = models.ForeignKey(Dataset,related_name="distributions")
	data_format = models.ForeignKey(Format,related_name="formatted_datasets",null=True,blank=True)
	#documentation_url = models.URLField(max_length=200,blank=True)

	def __unicode__(self):
		#return self.data_format.name
		return "({0}) {1}".format(self.data_format.name,self.dataset.title)

# The permissions model
class with_access(models.Model):
	ReadOnly = 'RO'
	ReadAndEdit = 'RW'
	ReadEditDelete = 'RX'
	ACCESS_LEVEL_CHOICES = (
		('RO','Read only'),
		('RW','Read and edit'),
		('RX','Read, edit and delete')
	)
	dataset = models.ForeignKey(Dataset, related_name='accessors')
	user = models.ForeignKey(Dataset, related_name='accessing')
	access_level = models.CharField(max_length=2,
                                      choices=ACCESS_LEVEL_CHOICES,
                                      default=ReadOnly)
	def can_edit(self):
		return self.access_level in (self.ReadAndEdit, self.ReadEditDelete)
	def can_delete(self):
		return self.access_level in (self.ReadEditDelete)

class DataRelation(models.Model):
	source = models.ForeignKey(Dataset, related_name='relation_to_derivative')
	derivative = models.ForeignKey(Dataset, related_name='relation_to_source')
	how_data_was_processed = models.TextField(max_length=20000,blank=True)
	processing_url = models.URLField(max_length=200,blank=True,null=True)

	def __unicode__(self):
		return self.source.title+" -> "+self.derivative.title


# The membership/organisation models

# This is a class to store a reference to a datascientist that's not registered as a user of the site
# This will be most of the scientists.
# Note that the natural key is first, last, and profile url. This should keep things more or less unique.
class ScientistManager(models.Manager):
	def get_by_natural_key(self,firstname,lastname,profile_url):
		return self.get(firstname=firstname,lastname=lastname,profile_url=profile_url)
class Scientist(models.Model):
	objects = ScientistManager()		# handles natural keys
	
	firstname = models.CharField(max_length=30)
	lastname = models.CharField(max_length=30,blank=True)
	user = models.OneToOneField(User,blank=True, null=True, related_name="scientist_profile")

	github_url = models.URLField(max_length=200,blank=True,default="")
	linkedin_url = models.URLField(max_length=200,blank=True,default="")
	profile_url = models.URLField(max_length=200,blank=True,default="")

	collaborators = models.ManyToManyField('self')

	class Meta:
		unique_together = (("firstname","lastname","profile_url"),)
	def __unicode__(self):
		return self.firstname+" "+self.lastname

class OrganizationManager(models.Manager):
	def get_by_natural_key(self,name):
		return self.get(name=name)
class Organization(models.Model):
	objects = OrganizationManager()		# handles natural keys

	name = models.CharField(max_length=200,unique=True)
	url = models.URLField(max_length=200,default="")
	
	members = models.ManyToManyField(Scientist, through='MembershipRelation')
	
	def __unicode__(self):
		return self.name

class MembershipRelation(models.Model):
	organization = models.ForeignKey(Organization, related_name='relation_to_member')
	member = models.ForeignKey(Scientist, related_name='relation_to_organization')

	def __unicode__(self):
		return self.member.firstname+" "+self.member.lastname+" -> "+self.organization.name
	
class ContributorRelation(models.Model):
	contributor = models.ForeignKey(Scientist, related_name='relation_to_data')
	dataset = models.ForeignKey(Dataset, related_name='relation_to_contributor')
	work_done = models.TextField(max_length=20000, blank=True)
	
	def __unicode__(self):
		return self.contributor.firstname+" "+self.contributor.lastname+ "-> "+self.contributor.firstname+" "+self.contributor.lastname	
	
	
	
	
	
	
	
	
