"""User generated post model."""

from django.db import models
from django.contrib.auth.models import User


def image_path(instance, file_name):
    """Upload file for user in media root."""
    return 'posts/images/{0}_{1}'.format(instance.image.id, file_name)


class Post(models.Model):
    """User generated post model."""

    author = models.OneToOneField(
        User,
        related_name='posts',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=75)
    content = models.TextField(max_length=15000)
    content_rendered = models.TextField(max_length=75000)
    url = models.CharField(max_length=500, null=True)
    image = models.ImageField(upload_to='image_path')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String Representation of post."""
        return str(self.title)


class Comment(models.Model):
    """Comment class."""

    on_post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    by_user = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    content = models.CharField(max_length=1028)

    def __str__(self):
        """String Representation of comment."""
        return str(self.content)


class Like(models.Model):
    """Comment class."""

    on_post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE,
    )
    by_user = models.ForeignKey(
        User,
        related_name='likes',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        """String Representation of like."""
        return str('Liked by ' + self.by_user.username)
