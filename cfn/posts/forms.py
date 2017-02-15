"""Add post form."""

from django import forms

from posts.models import Post


class AddPostForm(forms.ModelForm):
    """Form to add new album."""

    class Meta:
        """Define model and stuff."""

        model = Post
        exclude = [
            'date_uploaded',
            'date_modified',
            'author',
            'content_rendered',
        ]
