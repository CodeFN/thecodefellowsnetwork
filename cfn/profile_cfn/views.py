from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from profile_cfn.models import ProfileCfn
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, TemplateView):
    """Class based view for logged in user's profile."""

    login_url = '/'
    redirect_field_name = 'redirect_to'
    template_name = 'profile_cfn/profile.html'
    model = ProfileCfn

    def get_context_data(self, username=None):
        """Get profile information."""
        if self.request.user.is_authenticated():
            profile = self.request.user.profile
            return {
                'profile': profile,
            }


class ProfileViewOther(LoginRequiredMixin, DetailView):
    """"Profile view of other users."""

    login_url = '/'
    redirect_field_name = 'redirect_to'
    template_name = 'profile_cfn/profile.html'
    model = ProfileCfn
    slug_field = 'user__username'

    def get_context_data(self, **kwargs):
        """Get profile information and return it."""
        context = super(ProfileViewOther, self).get_context_data(**kwargs)
        profile = ProfileCfn.objects.get(user__username=self.kwargs['slug'])
        context['profile'] = profile
        return context
