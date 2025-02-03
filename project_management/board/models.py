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

class BoardLabel(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="labels")
    color = models.CharField(max_length=50)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class BoardMember(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="members")
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    deactivated = models.BooleanField(default=False)
    member_type = models.CharField(max_length=50)  # e.g. "admin", "editor", "viewer"
    unconfirmed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.member.full_name} in {self.board.title}"
    
class BoardAction(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="actions")
    member_creator = models.ForeignKey(Member, on_delete=models.CASCADE)
    data = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(max_length=50)  # e.g. "create_board", "delete_board"

    def __str__(self):
        return f"{self.action_type} by {self.member_creator.full_name}"