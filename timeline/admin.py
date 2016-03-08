from django.contrib import admin

# Register your models here.
from .models import Photo, Comment, User


class PhotoModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "timestamp", "user", "pk"]
	list_display_links = ["title"]
	list_filter = ["updated", "timestamp"]
	#list_editable = ["draft"]
	search_fields = ["title", "description"]
	ordering = ["timestamp"]

	class Meta:
		model = Photo


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email", "pk"]
    list_display_links = ["username"]
    list_filter = ["is_staff", "is_superuser"]
    ordering = ["id"]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Comment)