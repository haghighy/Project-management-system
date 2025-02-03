from django.db import models
from accounts.models import Member
from uuid import uuid4

class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    member_creator = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="created_boards")
    title = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    date_closed = models.DateTimeField(null=True, blank=True)
    date_last_view = models.DateTimeField(auto_now=True)
    date_last_activity = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shared_link = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.title
