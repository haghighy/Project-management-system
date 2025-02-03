from rest_framework import serializers
from .models import Comment
from cards.models import Card
from accounts.models import Member

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for adding and displaying comments on a card.
    """
    card_id = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all(), source="card", write_only=True)
    member_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), source="member", write_only=True)

    class Meta:
        model = Comment
        fields = ['card_id', 'member_id', 'comment', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        # Create comment logic
        return Comment.objects.create(**validated_data)
