from django.contrib import admin
from data_connections.models import Dataset, DataCatalog, DataRelation, License, Format, Organization, MembershipRelation, ContributorRelation, Scientist, Distribution, Keyword, Category

admin.site.register(Dataset)
admin.site.register(DataCatalog)
admin.site.register(DataRelation)
admin.site.register(License)
admin.site.register(Format)
admin.site.register(Organization)
admin.site.register(MembershipRelation)
admin.site.register(ContributorRelation)
admin.site.register(Scientist)
admin.site.register(Distribution)
admin.site.register(Keyword)
admin.site.register(Category)
