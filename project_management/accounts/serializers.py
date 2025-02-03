from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email_address", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        """
        Ensure passwords match.
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new user with a username based on the email.
        """
        email = validated_data["email_address"]
        username = email.split("@")[0]  # Extract first part of email
        password = validated_data.pop("password")
        validated_data.pop("password2")  # Remove password2 (not needed for User model)

        # Create User
        user = User.objects.create_user(username=username, email_address=email, password=password)

        return user

