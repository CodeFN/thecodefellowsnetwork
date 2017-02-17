from django.views.generic import UpdateView
from profile_cfn.models import ProfileCfn
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from profile_cfn.forms import EditProfileForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def ProfileView(request):
    """Profile view for loggin in user."""
    if request.user.is_authenticated():
        profile = get_object_or_404(ProfileCfn.objects, user__username=request.user.username)
        all_follows = profile.follows.all()
        all_followed_by = profile.followed_by.all()
        follows_page = request.GET.get("follows_page", 1)
        followed_page = request.GET.get("followed_page", 1)

        follows_pages = Paginator(all_follows, 12)
        followed_pages = Paginator(all_followed_by, 12)

        try:
            follows = follows_pages.page(follows_page)
            followed_by = followed_pages.page(followed_page)
        except PageNotAnInteger:
            follows = follows_pages.page(1)
            followed_by = followed_pages.page(1)
        except EmptyPage:
            follows = follows_pages.page(follows_pages.num_pages)
            followed_by = followed_pages.page(followed_pages.num_pages)
        return render(request, "profile_cfn/profile.html", {
            'profile': profile,
            'follows': follows,
            'followed_by': followed_by,
        })


@login_required
def ProfileViewOther(request, slug):
    """Profile view for other user."""
    if request.user.is_authenticated():
        user_follows = request.user.profile.follows.all()
        profile = get_object_or_404(ProfileCfn.objects, user__username=slug)
        all_follows = profile.follows.all()
        all_followed_by = profile.user.followed_by.all()
        follows_page = request.GET.get("follows_page", 1)
        followed_page = request.GET.get("followed_page", 1)

        follows_pages = Paginator(all_follows, 12)
        followed_pages = Paginator(all_followed_by, 12)

        try:
            follows = follows_pages.page(follows_page)
            followed_by = followed_pages.page(followed_page)
        except PageNotAnInteger:
            follows = follows_pages.page(1)
            followed_by = followed_pages.page(1)
        except EmptyPage:
            follows = follows_pages.page(follows_pages.num_pages)
            followed_by = followed_pages.page(followed_pages.num_pages)
        if request.method == 'POST':
            to_follow = User.objects.get(username=slug)
            if to_follow in user_follows:
                request.user.profile.follows.remove(to_follow)
            else:
                request.user.profile.follows.add(to_follow)
            return HttpResponseRedirect("/profile/" + slug)
        return render(request, "profile_cfn/profile.html", {
            'profile': profile,
            'follows': follows,
            'followed_by': followed_by,
            'user_follows': user_follows,
        })


class EditProfileView(LoginRequiredMixin, UpdateView):
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
        self.object.user.profile.save()
        self.object.user.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
