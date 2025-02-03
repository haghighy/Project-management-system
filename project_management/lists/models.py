from uuid import uuid4
from django.db import models
from board.models import Board

class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")
    name = models.CharField(max_length=255)
    position = models.PositiveIntegerField()
    is_closed = models.BooleanField(default=False)
    date_closed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
