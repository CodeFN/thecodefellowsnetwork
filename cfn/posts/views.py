"""Post views."""

# from django.shortcuts import render
from django.views.generic import ListView

from posts.models import Post


class PostsView(ListView):
    """Posts View."""

    template_name = 'posts/posts.html'

    def get_context_data(self):
        """."""
        posts = []
        user = self.request.user
        following = []
        for user in user.follows:
            following.append(user.username)
        all_posts = Post.objects.all()
        for post in all_posts:
            if post.author.username in following:
                posts.append(post)
        return {'posts': posts}

    def get_queryset(self):
        """."""
        return {}


class PostView(ListView):
    """."""

    pass


class NewPostView(ListView):
    """."""

    pass


class EditPostView(ListView):
    """."""

    pass
