from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ProfileCfn(models.Model):
    """The profile for a CFN user."""

    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
    )
    profile_picture = models.ImageField(upload_to='profile_picture')
    about = models.TextField(max_length=1028, blank=True)
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
    )
