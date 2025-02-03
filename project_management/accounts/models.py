from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        swappable = 'AUTH_USER_MODEL' 


class Member(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile" 
    )
    email_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    full_name_privacy = models.BooleanField(default=True) 
    job_title = models.CharField(max_length=255, blank=True, null=True)

    @property
    def full_name(self):
        if self.full_name_privacy:
            return self.user.username
        return f"{self.user.first_name} {self.user.last_name}".strip()

    def __str__(self):
        return f"{self.user.username} ({self.full_name})"
