from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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


@receiver(post_save, sender=User)
def make_user_profile(sender, instance, **kwargs):
    """Create and save a profile when a user is created."""
    if kwargs["created"]:
        profile = ProfileCfn(user=instance)
        profile.save()
