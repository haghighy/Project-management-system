from rest_framework import serializers
from .models import Board, BoardLabel, BoardMember


from rest_framework import serializers
from .models import Board, BoardLabel, BoardMember
from accounts.models import Member


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating boards.
    """
    member_creator = serializers.IntegerField()

    class Meta:
        model = Board
        fields = ['member_creator', 'title', 'is_public', 'is_closed', 'date_closed', 'date_last_view',
                  'date_last_activity', 'description', 'created_at', 'shared_link']

    def create(self, validated_data):
        member_creator_id = validated_data.pop('member_creator')
        member_creator = Member.objects.get(id=member_creator_id) 

        board = Board.objects.create(member_creator=member_creator, **validated_data)  
        return board



class BoardLabelSerializer(serializers.ModelSerializer):
    """
    Serializer for adding labels to boards.
    """
    board_id = serializers.CharField(write_only=True)

    class Meta:
        model = BoardLabel
        fields = ['board_id', 'color', 'name']

    def create(self, validated_data):
        board_id = validated_data.pop('board_id') 
        board = Board.objects.get(id=board_id) 
        label = BoardLabel.objects.create(board=board, **validated_data) 
        return label


class BoardMemberSerializer(serializers.ModelSerializer):
    """
    Serializer for adding members to boards.
    """
    member_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BoardMember
        fields = ['id', 'member_id', 'deactivated', 'member_type', 'unconfirmed']

    def create(self, validated_data):
        member_id = validated_data.pop('member_id')  # Extract the member_id
        member = Member.objects.get(id=member_id)  # Get the Member object based on the id
        board_member = BoardMember.objects.create(member=member, **validated_data)  # Create the board member and associate it
        return board_member
