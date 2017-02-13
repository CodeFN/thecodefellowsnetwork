from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from profile_cfn.models import ProfileCfn


class ProfileCfnView(TemplateView):
    """Class based view for logged in user's profile."""

    template_name = 'profile_cfn/profile_cfn.html'

    def get_context_data(self, username=None):
        """Get profile information."""
        if self.request.user.is_authenticated():
            profile = self.request.user.profile
            return {
                'profile': profile,
            }
        else:
            error_message = "You must sign in to do that!"
            return {'error': error_message}
