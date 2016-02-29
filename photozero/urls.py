from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

import timeline.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', timeline.views.photo_list, name='list'),
    url(r'^timeline/', include('timeline.urls', namespace='timeline')),
    url(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)