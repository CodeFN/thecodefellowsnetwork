"""Add post form."""

from django import forms


from posts.models import Post, Comment


class AddPostForm(forms.ModelForm):
    """Form to add new post."""

    class Meta:
        """Define model and stuff."""

        model = Post
        exclude = [
            'date_uploaded',
            'date_modified',
            'author',
        ]


class EditPostForm(forms.ModelForm):
    """Form to edit existing post."""

    class Meta:
        """Define model and stuff."""

        model = Post
        exclude = [
            'date_uploaded',
            'date_modified',
            'author',
        ]


class CommentForm(forms.ModelForm):
    """Form to post a comment."""

    class Meta:
        """Define model and stuff."""

        model = Comment
        exclude = [
            'by_user',
            'on_post',
            'datetime',
        ]
