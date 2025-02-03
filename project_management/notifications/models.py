from django.db import models
from accounts.models import Member
from board.models import Board
from cards.models import Card

class Notification(models.Model):
    recipient = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="notifications_sent")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)  # "card_assigned", "comment", etc.
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.recipient.username}: {self.message[:50]}"
