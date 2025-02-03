from rest_framework import serializers
from .models import List

class ListSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating lists.
    """
    class Meta:
        model = List
        fields = ['id', 'board', 'name', 'position', 'is_closed', 'date_closed']
        read_only_fields = ['date_closed']  
