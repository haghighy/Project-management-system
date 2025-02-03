from uuid import uuid4
from django.db import models
from lists.models import List
from board.models import Board, BoardLabel
from accounts.models import Member

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
    

class CardMember(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="members")
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.member.full_name} in {self.card.title}"


class CardLabel(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="labels")
    board_label = models.ForeignKey(BoardLabel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Label for {self.card.title}"

class CardAction(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="actions")
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    data = models.JSONField()
    date = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.action_type} by {self.member.full_name}"