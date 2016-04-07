from urllib import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from .forms import PhotoForm, CommentForm
from .models import Photo, Comment

def photo_test(request):
	return HttpResponse("<h2>Test View Works!!</h2>")

def photo_list(request):
	queryset_list = Photo.objects.all()
	query = request.GET.get("q")
	
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(description__icontains=query) |
			Q(user__username__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query) |
			Q(tags__name__in=[query])
			).distinct()

	context = {
		"object_list": queryset_list,
		"title": "PhotoZero",
	}

	return render(request, "photo_list.html", context)


def photo_detail(request, slug=None):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/accounts/login")

	instance = get_object_or_404(Photo, slug=slug)

	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
		    comment = form.save(commit=False)
		    comment.author = request.user
		    comment.post = instance
		    comment.save()
		    messages.success(request, "Comment Added") # message success
		    return redirect('timeline:detail', slug=instance.slug)
	else:
		form = CommentForm()

	share_string = quote_plus(instance.description)

	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
		"form": form,
	}

	return render(request, "photo_detail.html", context)   


def photo_create(request):
	if not request.user.is_authenticated():
	 	return HttpResponseRedirect("/accounts/login")

	form = PhotoForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		form.save_m2m()
		messages.success(request, "Succesfully Uploaded") # message success

		return HttpResponseRedirect(instance.get_absolute_url())
		
	context = {
		"form": form,
	}

	return render(request, "photo_upload.html", context)


def photo_update(request, slug=None):
	if not request.user.is_authenticated():
	 	return HttpResponseRedirect("/accounts/login")

	instance = get_object_or_404(Photo, slug=slug)
	form = PhotoForm(request.POST or None, request.FILES or None, instance=instance)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		form.save_m2m()
		messages.success(request, "Succesfully Updated") # message success

		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}

	return render(request, "photo_update.html", context)


def photo_delete(request, slug=None):
	if not request.user.is_authenticated():
	 	return HttpResponseRedirect("/accounts/login")

	instance = get_object_or_404(Photo, slug=slug)
	instance.delete()
	messages.success(request, "Succesfully Deleted")

	return redirect("timeline:list")


def license(request):
	return render(request, "license.html")


def like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        photo = get_object_or_404(Photo, slug=slug)

        if photo.likes.filter(id=user.id).exists():
            # user has already liked this photo
            # remove like/user
            photo.likes.remove(user)
            action = 'disliked'
        else:
            # add a new like for this photo
            photo.likes.add(user)
            action = 'liked'

    context = {'likes_count': photo.total_likes(), 'action': action}
    return JsonResponse(context)
















