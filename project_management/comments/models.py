from uuid import uuid4
from django.db import models
from cards.models import Card
from accounts.models import Member

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="comments")
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:50]
