"""Group forms."""

from django import forms
from django.contrib.auth.models import User, Group


class CreateGroupForm(forms.ModelForm):
    """Form to createa group."""

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super(CreateGroupForm, self).__init__(*args, **kwargs)
        self.fields["First Name"] = forms.CharField(initial=self.instance.user.first_name)
        pass

    class Meta:
        """Define model."""

        model = Group

        pass


class AddUserForm(forms.ModelForm):
    """Form to createa group."""

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        pass

    class Meta:
        """Define model."""

        pass



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


from django import forms
from profile_cfn.models import ProfileCfn


class EditProfileForm(forms.ModelForm):
    """Form to add new album."""

    def __init__(self, *args, **kwargs):
        """Setup the form fields."""
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["First Name"] = forms.CharField(initial=self.instance.user.first_name)
        self.fields["Last Name"] = forms.CharField(initial=self.instance.user.last_name)
        del self.fields["user"]
        for field in self.fields:
            self.fields[field].required = False

    class Meta:

        model = ProfileCfn
        exclude = ['follows', 'avatar_url', 'github_url']
