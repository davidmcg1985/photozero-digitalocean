from django import forms
from django.template.defaultfilters import filesizeformat
from .models import Photo, Comment


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            "title",
            "description",
            "image",
        ]


class CommentForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea, label='Leave a comment: ')
	class Meta:
		model = Comment
		fields = [
			"text",
		]