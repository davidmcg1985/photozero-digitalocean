from urllib import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import PhotoForm, CommentForm
from .models import Photo, Comment


def photo_list(request):

	queryset_list = Photo.objects.all()

	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Photo.objects.all()

	query = request.GET.get("search")

	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(description__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query) |
			# Q(tags__icontains=query) |
			Q(tags__name__in=[query])
			).distinct()

	paginator = Paginator(queryset_list, 10) # Show 10 items per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    queryset = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    queryset = paginator.page(paginator.num_pages)

	context = {
		"object_list": queryset,
		"title": "PhotoZone",
		"page_request_var": page_request_var,
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
		    return redirect('timeline:detail', slug=instance.slug)
	else:
		form = CommentForm()

	share_string = quote_plus(instance.description)
	# number_of_likes = instance.likes.all().count()

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
		messages.success(request, "Succesfully Created") # message success

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
		# instance.user = request.user
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


def like(request, slug=None):
    if request.method == 'POST':
        user = request.user
        # slug = request.POST.get('slug', None)
        photo = get_object_or_404(Photo, slug=slug)

        if photo.likes.filter(id=user.id).exists():
            # user has already liked this company
            # remove like/user
            photo.likes.remove(user)
            message = 'You disliked this'
        else:
            # add a new like for a company
            photo.likes.add(user)
            message = 'You liked this'

    context = {'likes_count': photo.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(context), content_type='application/json')
















