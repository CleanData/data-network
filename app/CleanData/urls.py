from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
	url(r'frontpage','views.frontpage',name='front'),
    (r'', include('CleanData.data_connections.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# (r'^accounts/register/','registration_app.views.register')
	(r'^accounts/', include('registration.backends.default.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^profile/$',include())
)
