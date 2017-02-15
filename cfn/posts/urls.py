"""Posts URL Configuration."""

from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from posts.views import (
    PostsView,
    PostView,
    NewPostView,
    EditPostView,
)

urlpatterns = [
    url(r'^$', PostsView.as_view(), name='posts'),
    url(r'^(?P<pk>\d+)$', PostView.as_view(), name='post'),
    url(r'^new/$', NewPostView.as_view(), name='new_post'),
    url(r'^(?P<pk>\d+)/edit$', EditPostView.as_view(), name='edit_post'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
