from rest_framework import exceptions, serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

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


class UserSerializerWithToken(serializers.Serializer):
    """
    Serializer to include JWT access and refresh tokens with user data.
    """
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    def get_access(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to authenticate users using username or email and return JWT tokens.
    """
    def validate(self, data):
        password = data.get("password")
        username = data.get("username")
        user = User.objects.filter(
            Q(username__iexact=username) | Q(email_address__iexact=username),
            is_active=True,
        ).first()
        if not user or not user.check_password(password):
            raise exceptions.AuthenticationFailed("No account found with the given credentials.")

        return UserSerializerWithToken(user).data
