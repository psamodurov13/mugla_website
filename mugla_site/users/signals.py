from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(instance)
        print(instance.__dict__)
        new_profile = Profile.objects.create(user=instance)
        new_profile.slug = instance.username
        new_profile.save()


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
