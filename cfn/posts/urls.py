"""Posts URL Configuration."""

from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from posts.views import PostsView

urlpatterns = [
    url(r'^$', PostsView.as_view(), name='posts'),
    url(r'^$', PostsView.as_view(), name='posts'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
