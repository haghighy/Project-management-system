from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Member

User = get_user_model()

@receiver(post_save, sender=User)
def create_member_for_new_user(sender, instance, created, **kwargs):
    """
    Create a Member instance automatically when a new User is created.
    """
    if created:
        Member.objects.create(user=instance)
