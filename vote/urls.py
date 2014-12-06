from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vote.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^post/', post),
    url(r'^candidates', get_candidates),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
