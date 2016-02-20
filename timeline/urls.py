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
    # url(r'^(?P<slug>[\w-]+)/comment/$', photo_comment, name='comment'),

    # url(r'^post/(?P<pk>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
]