from django.views.generic import TemplateView, DetailView
from profile_cfn.models import ProfileCfn
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


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
            follows = profile.follows.all()
            followed_by = self.request.user.followed_by.all()
            return {
                'profile': profile,
                'follows': follows,
                'followed_by': followed_by,
            }
        else:
            error_message = "You must sign in to do that!"
            return {'error': error_message}

    def __str__(self):
        """String representation of a user profile."""
        return self.user


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
        follows = profile.follows.all()
        followed_by = profile.user.followed_by.all()
        user_follows = self.request.user.profile.follows.all()
        context['profile'] = profile
        context['follows'] = follows
        context['followed_by'] = followed_by
        context['user_follows'] = user_follows
        return context

    def post(self, request, *args, **kwargs):
        to_follow = User.objects.get(username=kwargs['slug'])
        followed_list = self.request.user.profile.follows.all()
        if to_follow in followed_list:
            self.request.user.profile.follows.remove(to_follow)
        else:
            self.request.user.profile.follows.add(to_follow)
        return HttpResponseRedirect("/profile/" + kwargs['slug'])
