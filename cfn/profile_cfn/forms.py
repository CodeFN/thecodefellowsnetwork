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
