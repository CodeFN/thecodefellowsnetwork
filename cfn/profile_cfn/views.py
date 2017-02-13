from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from profile_cfn.models import ProfileCfn


class ProfileView(TemplateView):
    """Class based view for logged in user's profile."""

    template_name = 'profile_cfn/profile.html'
    model = ProfileCfn

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


class ProfileViewOther(DetailView):
    """"Profile view of other users."""

    template_name = 'profile_cfn/profile.html'
    model = ProfileCfn
    slug_field = 'user__username'

    def get_context_data(self, **kwargs):
        """Get profile information and return it."""
        context = super(ProfileViewOther, self).get_context_data(**kwargs)
        profile = ProfileCfn.objects.get(user__username=self.kwargs['slug'])
        context['profile'] = profile
        return context