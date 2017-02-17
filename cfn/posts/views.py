"""Post views."""

from django.http import Http404, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView

from posts.models import Post
from posts.forms import AddPostForm, EditPostForm, CommentForm

from django.contrib.auth.mixins import LoginRequiredMixin


class PostsView(LoginRequiredMixin, ListView):
    """Posts View."""

    login_url = '/'
    redirect_field_name = 'redirect_to'
    template_name = 'posts/posts.html'

    def get_context_data(self):
        """Get the posts."""
        all_posts = Post.objects.all().order_by('-id')
        return {'posts': all_posts}

    def get_queryset(self):
        """Return an empty dictionary."""
        return {}


class PostView(LoginRequiredMixin, DetailView):
    """View an individual post."""

    login_url = '/'
    redirect_field_name = 'redirect_to'
    template_name = 'posts/post.html'
    model = Post

    def get_object(self, queryset=None):
        """Get the post to view."""
        post = Post.objects.get(id=self.kwargs['pk'])
        return post

    def get_context_data(self, **kwargs):
        """Return the comment form."""
        context = super(PostView, self).get_context_data(**kwargs)
        context['form'] = CommentForm
        return context


class NewCommentView(SingleObjectMixin, FormView):
    """Handle comment view."""

    template_name = 'posts/post.html'
    form_class = CommentForm
    model = Post

    def form_valid(self, form):
        """Check if the form is valid."""
        form.instance.by_user = self.request.user
        form.instance.on_post = self.object
        form.save()
        return super(NewCommentView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """Post comment method."""
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super(
            NewCommentView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """Redirect after success."""
        return reverse_lazy(
            'post', kwargs={'pk': self.object.pk})


class PostWithCommentsView(View):
    """Post view including comments."""

    def get(self, request, *args, **kwargs):
        """Get request."""
        view = PostView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post request."""
        view = NewCommentView.as_view()
        return view(request, *args, **kwargs)


class NewPostView(LoginRequiredMixin, CreateView):
    """View for creating a new post."""

    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = Post
    template_name = "posts/new_post.html"
    success_url = reverse_lazy('posts')
    form_class = AddPostForm

    def form_valid(self, form):
        """Check if the form is valid."""
        form.instance.author = self.request.user
        return super(NewPostView, self).form_valid(form)


class EditPostView(LoginRequiredMixin, UpdateView):
    """Edit an existing post."""

    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = Post
    template_name = "posts/edit_post.html"
    success_url = reverse_lazy('posts')
    form_class = EditPostForm

    def get_object(self, queryset=None):
        """Get the post to edit."""
        post_to_edit = Post.objects.get(id=self.kwargs['pk'])
        if not post_to_edit.author == self.request.user:
            raise Http404
        return post_to_edit

    def form_valid(self, form):
        """Check if the form is valid."""
        form.instance.author = self.request.user
        return super(EditPostView, self).form_valid(form)


class DeletePostView(LoginRequiredMixin, DeleteView):
    """Delete a post."""

    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = Post
    success_url = reverse_lazy('posts')
    template_name = 'posts/confirm_delete.html'

    def get_object(self, queryset=None):
        """Get the post to delete."""
        post_to_delete = Post.objects.get(id=self.kwargs['pk'])
        if not post_to_delete.author == self.request.user:
            raise Http404
        return post_to_delete
