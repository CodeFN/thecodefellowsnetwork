"""User generated post model."""

from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager


def image_path(instance, file_name):
    """Upload file for user in media root."""
    return 'posts/images/{0}_{1}'.format(instance.image.id, file_name)


class Post(models.Model):
    """User generated post model."""

    author = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=75, default='Note')
    content = models.TextField(max_length=15000)
    url = models.URLField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='image_path', null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String Representation of post."""
        return str(self.title)

    objects = InheritanceManager()


class Idea(Post):
    """An idea."""

    test = models.CharField(max_length=10, default='testField')

    def save(self, *args, **kwargs):
        self.category = 'Idea'
        super(Idea, self).save(*args, **kwargs)


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
    comment = models.CharField(max_length=1028)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String Representation of comment."""
        return str(self.comment)
