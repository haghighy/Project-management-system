from rest_framework import exceptions, serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import Member

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

class RequestResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for handling password reset requests.
    Validates if the provided email exists in the system.
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email_address=value).exists():
            raise exceptions.ValidationError("User with this email was not found.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for resetting the user's password.
    Validates the token, user ID, and password confirmation.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[django_validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")
        token = data.get("token")
        uidb64 = data.get("uidb64")

        if password != password2:
            raise exceptions.ValidationError("Passwords do not match.")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise exceptions.ValidationError("The reset link is invalid.")

        if not default_token_generator.check_token(user, token):
            raise exceptions.ValidationError("The reset link is invalid.")

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["password"])
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating user profile details.
    """
    full_name = serializers.CharField(source='profile.full_name', read_only=True)
    bio = serializers.CharField(source='profile.bio', allow_blank=True, required=False)
    avatar_url = serializers.URLField(source='profile.avatar_url', allow_blank=True, required=False)
    full_name_privacy = serializers.BooleanField(source='profile.full_name_privacy', required=False)
    job_title = serializers.CharField(source='profile.job_title', allow_blank=True, required=False)

    class Meta:
        model = User
        fields = ['email_address', 'username', 'first_name', 'last_name', 'full_name', 'bio', 'avatar_url', 'full_name_privacy', 'job_title']
        read_only_fields = ['email_address']

    def update(self, instance, validated_data):
        user_fields = ['username', 'first_name', 'last_name']
        for field in user_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        profile_data = validated_data.get('profile', {})
        member = instance.profile
        member_fields = ['bio', 'avatar_url', 'full_name_privacy', 'job_title']
        for field in member_fields:
            if field in profile_data:
                setattr(member, field, profile_data[field])

        instance.save()
        member.save()
        return instance