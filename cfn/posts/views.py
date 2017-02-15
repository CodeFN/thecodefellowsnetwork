"""Post views."""

# from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from posts.models import Post
from posts.forms import AddPostForm


class PostsView(ListView):
    """Posts View."""

    template_name = 'posts/posts.html'

    def get_context_data(self):
        """."""
        all_posts = Post.objects.all()
        return {'posts': all_posts}

    def get_queryset(self):
        """."""
        return {}


class PostView(ListView):
    """."""

    template_name = 'posts/post.html'
    model = Post

    def get_context_data(self):
        """."""
        self.post = Post.objects.get(id=self.kwargs['pk'])
        return {'post': self.post}


class NewPostView(CreateView):
    """."""

    template_name = "posts/new_post.html"
    model = Post
    success_url = reverse_lazy('posts')
    form_class = AddPostForm

    def form_valid(self, form):
        """."""
        form.instance.author = self.request.user
        return super(NewPostView, self).form_valid(form)


class EditPostView(ListView):
    """."""

    pass
