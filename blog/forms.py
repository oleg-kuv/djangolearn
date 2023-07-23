from django import forms
from django.contrib.auth.models import User
from .models import Post, Tag


class PostForm (forms.ModelForm):
    def __init__(self, data=None, user: User = None, * args, **kwargs):
        super().__init__(data, **kwargs)
        self.fields['tags'].queryset = Tag.objects.filter(author=user)

    class Meta:
        model = Post
        fields = ('active', 'title', 'text', 'tags')
