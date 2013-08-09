from django.contrib import admin
from data_connections.models import Dataset, DataCatalog, DataRelation, License, Format, UserProfile, Organization, MembershipRelation, ContributorRelation, Scientist

#remove comment for custom fields
#class DatasetAdmin(admin.ModelAdmin):
	#fields = ['name', 'url', 'data_format', 'date_published', 'date_last_edited','license','manager','managing_organization']

admin.site.register(Dataset)
admin.site.register(DataCatalog)
admin.site.register(DataRelation)
admin.site.register(License)
admin.site.register(Format)
admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(MembershipRelation)
admin.site.register(ContributorRelation)
admin.site.register(Scientist)
