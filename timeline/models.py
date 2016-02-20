from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils import timezone

from imagekit.models import ProcessedImageField
from imagekit.processors import Transpose, ResizeToFit

from django.utils.text import slugify

import hashlib


def upload_location(instance, filename):
	return "%s/%s" %(instance.slug, filename)


class Photo(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	image = ProcessedImageField(upload_to=upload_location, 
		null=True, 
		blank=False,
		processors=[Transpose(), ResizeToFit(1000, 1000, False)],
		format='JPEG',
		options={'quality': 50},
		width_field="width_field",
		height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	description = models.TextField(max_length=1000)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("timeline:detail", kwargs={"slug": self.slug})

	class Meta:
		ordering = ["-timestamp", "-updated"]


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Photo.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Photo)


class Comment(models.Model):
    post = models.ForeignKey('timeline.Photo', related_name='comments')
    author = models.ForeignKey(User, related_name='comment_set')
    text = models.TextField(max_length=1000)
    created_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.text

