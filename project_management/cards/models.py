from uuid import uuid4
from django.db import models
from lists.models import List
from board.models import Board

class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="cards")
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="cards")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    reminder_date = models.DateTimeField(null=True, blank=True)
    position = models.PositiveIntegerField()

    def __str__(self):
        return self.title
