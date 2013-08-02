from django.conf.urls.defaults import *
from registration.backends.default.views import RegistrationView


urlpatterns = patterns('registration_app.views',
    url(r'^registration/', 'registration'),
    (r'^',include('registration.backends.default.urls')),
)