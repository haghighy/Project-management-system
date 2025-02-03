from rest_framework.serializers import ModelSerializer


class UserRegisterSerializer(ModelSerializer):
    """
    Serializer for user registration.
    """
 
    
class UserSerializerWithToken(ModelSerializer):
    """
    Serializer for email activation."
    """