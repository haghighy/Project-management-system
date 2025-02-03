from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying and managing notifications.
    """
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'board', 'card', 'type', 'message', 'is_read', 'created_at']
        read_only_fields = ['created_at', 'is_read']
