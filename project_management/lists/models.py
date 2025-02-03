from uuid import uuid4
from django.db import models
from board.models import Board
from accounts.models import Member

class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")
    name = models.CharField(max_length=255)
    position = models.PositiveIntegerField()
    is_closed = models.BooleanField(default=False)
    date_closed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class ListAction(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="actions")
    member_creator = models.ForeignKey(Member, on_delete=models.CASCADE)
    data = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.action_type} by {self.member_creator.full_name}"