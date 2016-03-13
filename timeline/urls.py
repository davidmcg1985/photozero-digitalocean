from django.conf.urls import url
from django.contrib import admin

from .views import (
	photo_list,
	photo_create,
	photo_detail,
	photo_update,
	photo_delete,
	)

urlpatterns = [
    url(r'^$', photo_list, name='list'),
    url(r'^create/$', photo_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', photo_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', photo_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', photo_delete, name='delete'),
]