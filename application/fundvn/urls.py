from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
	    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
	    (r'^', include('fundvn.main.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('registration.urls')),

)
