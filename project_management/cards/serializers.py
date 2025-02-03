from rest_framework import serializers
from .models import Card, CardLabel, CardMember, CardAction
from accounts.models import User, Member

class CardSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating cards.
    """
    class Meta:
        model = Card
        fields = ['id', 'board', 'list', 'title', 'description', 'created_at', 'due_date', 'reminder_date', 'position']
        
class CardLabelSerializer(serializers.ModelSerializer):
    """
    Serializer for adding labels to cards.
    """
    card_id = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all(), source="card", write_only=True)

    class Meta:
        model = CardLabel
        fields = ['id', 'card_id', 'board_label']

class CardMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for adding members to cards.
    """
    card_id = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all(), source="card", write_only=True)
    member_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), source="member", write_only=True)

    class Meta:
        model = CardMember
        fields = ['id', 'card_id', 'member_id']

class CardActionSerializer(serializers.ModelSerializer):
    """
    Serializer for actions taken on cards.
    """
    card_id = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all(), source="card", write_only=True)
    member_id = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), source="member", write_only=True)

    class Meta:
        model = CardAction
        fields = ['id', 'card_id', 'member_id', 'data', 'date', 'action_type']
