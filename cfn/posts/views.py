"""Post views."""

from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView

from posts.models import Post
from posts.forms import AddPostForm, EditPostForm


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

    model = Post
    template_name = "posts/new_post.html"
    success_url = reverse_lazy('posts')
    form_class = AddPostForm

    def form_valid(self, form):
        """."""
        form.instance.author = self.request.user
        return super(NewPostView, self).form_valid(form)


class EditPostView(UpdateView):
    """."""

    model = Post
    template_name = "posts/edit_post.html"
    success_url = reverse_lazy('posts')
    form_class = EditPostForm

    def get_object(self, queryset=None):
        """."""
        post_to_edit = Post.objects.get(id=self.kwargs['pk'])
        if not post_to_edit.author == self.request.user:
            raise Http404
        return post_to_edit

    def form_valid(self, form):
        """."""
        form.instance.author = self.request.user
        return super(EditPostView, self).form_valid(form)


class DeletePostView(DeleteView):
    """Delete a post."""

    model = Post
    success_url = reverse_lazy('posts')
    template_name = 'posts/confirm_delete.html'

    def get_object(self, queryset=None):
        """Get the post to delete."""
        post_to_delete = Post.objects.get(id=self.kwargs['pk'])
        if not post_to_delete.author == self.request.user:
            raise Http404
        return post_to_delete
