from django.views.generic import TemplateView, DetailView, UpdateView
from profile_cfn.models import ProfileCfn
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from profile_cfn.forms import EditProfileForm
from django.urls import reverse_lazy


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


class EditProfileView(UpdateView):
    """Update profile."""

    login_required = True
    template_name = 'profile_cfn/edit_profile.html'
    success_url = reverse_lazy('profile_self')
    form_class = EditProfileForm
    model = ProfileCfn

    def get_object(self):
        """Define what profile to edit."""
        return self.request.user.profile

    def form_valid(self, form):
        """If form post is successful."""
        self.object = form.save()
        self.object.user.first_name = form.cleaned_data['First Name']
        self.object.user.last_name = form.cleaned_data['Last Name']
        self.object.user.profile.about = form.cleaned_data['about']
        self.object.user.profile.profile_picture = form.cleaned_data['profile_picture']
        self.object.user.profile.save()
        self.object.user.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())