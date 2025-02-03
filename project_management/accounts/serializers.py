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
    Serializer that returns JWT tokens if the email is verified,
    otherwise, it returns only email verification status and email address.
    """
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()
    email_verified = serializers.SerializerMethodField()
    email_address = serializers.SerializerMethodField()

    def to_representation(self, obj):
        print(obj.profile.email_verified)
        if obj.profile.email_verified:
            return {
                "access": self.get_access(obj),
                "refresh": self.get_refresh(obj)
            }
        return {
            "email_verified": obj.profile.email_verified,
            "email_address": obj.email_address
        }

    def get_access(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)

    def get_email_verified(self, obj):
        return obj.profile.email_verified

    def get_email_address(self, obj):
        return obj.email_address


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
    
    
from django.contrib.auth.password_validation import validate_password as django_validate_password
from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[django_validate_password])
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Ensure `new_password` and `new_password2` match.
        """
        new_password = data.get("new_password")
        new_password2 = data.get("new_password2")
        
        missing_fields = [field for field in ["old_password", "new_password", "new_password2"] if not data.get(field)]
        if missing_fields:
            raise exceptions.ValidationError({field: "This field is required." for field in missing_fields})

        if new_password != new_password2:
            raise serializers.ValidationError({"new_password2": "New passwords must match."})

        return data
    
class ChangeEmailSerializer(serializers.Serializer):
    """
    Serializer to handle changing email address.
    """
    new_email = serializers.EmailField(required=True)
    confirm_new_email = serializers.EmailField(required=True)

    def validate(self, attrs):
        new_email = attrs.get("new_email")
        confirm_new_email = attrs.get("confirm_new_email")

        if new_email != confirm_new_email:
            raise ValidationError("Email addresses must match.")
        
        if new_email == self.context['request'].user.email_address:
            raise ValidationError("The new email must be different from the current email address.")

        if User.objects.filter(email_address=new_email).exists():
            raise ValidationError("This email address is already in use.")

        return attrs