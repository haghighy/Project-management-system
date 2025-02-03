from rest_framework import serializers
from .models import Board, BoardLabel, BoardMember


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating boards.
    """
    member_creator = serializers.PrimaryKeyRelatedField(queryset=BoardMember.objects.all(), write_only=True)

    class Meta:
        model = Board
        fields = ['id', 'member_creator', 'title', 'is_public', 'is_closed', 'date_closed', 'date_last_view',
                  'date_last_activity', 'description', 'created_at', 'shared_link']


class BoardLabelSerializer(serializers.ModelSerializer):
    """
    Serializer for adding labels to boards.
    """
    board_id = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all(), source="board", write_only=True)
    
    class Meta:
        model = BoardLabel
        fields = ['id', 'board_id', 'color', 'name']


class BoardMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for adding members to boards.
    """
    member_id = serializers.PrimaryKeyRelatedField(queryset=BoardMember.objects.all(), source="member", write_only=True)
    
    class Meta:
        model = BoardMember
        fields = ['id', 'member_id', 'deactivated', 'member_type', 'unconfirmed']
