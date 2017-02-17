"""Views for CFN."""
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from posts.models import Post


class HomeView(TemplateView):
    """Home View."""

    template_name = 'cfn/home.html'

    def get_context_data(self):
        """Get the posts of all users followed by logged in user."""
        if self.request.user.is_authenticated:
            the_followed = self.request.user.profile.follows.all()
            feed_posts = Post.objects.filter(author=self.request.user)
            for fellow in the_followed:
                fellow_posts = fellow.posts.all()
                feed_posts = feed_posts | fellow_posts
            feed_posts = feed_posts.order_by('date_modified').reverse()
            return {'feed_posts': feed_posts}


class FindUserView(ListView):
    """Class-based view for my list of user profiles."""

    model = User
    template_name = "cfn/find_user.html"
    context_object_name = "fellows"
    paginate_by = 72
    queryset = User.objects.all().order_by('username')


class AboutView(TemplateView):
    """About View."""

    template_name = 'cfn/about.html'
