"""Add post form."""

from django import forms


from posts.models import Post, Comment


class AddPostForm(forms.ModelForm):
    """Form to add new post."""

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super(AddPostForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = None
        self.fields['category'].initial = 'Note'
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, forms.TypedChoiceField):
                field.choices = field.choices[1:]

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
