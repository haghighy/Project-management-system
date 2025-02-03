from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserRegisterSerializer, 
    MyTokenObtainPairSerializer, 
    RequestResetPasswordSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from .utils import activation_mail, reset_password_mail, Util

User = get_user_model()


class RegisterAPIView(APIView):
    """
    This endpoint allows clients to register a new user and sends 
    an activation email.
    """

    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            try:
                email_data = activation_mail(user)
                Util.send_email(email_data)
            except Exception as e:
                return Response(
                    {"message": "User registered, but activation email could not be sent."},
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {"message": "Registration successful. Check your email for activation link."},
                status=status.HTTP_201_CREATED,
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ActivateEmailAPIView(APIView):
    """
    Activates a user account if the provided token is valid.
    """

    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.profile.email_verified = True
                user.profile.save()
                return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)

            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except (User.DoesNotExist, ValueError):
            return Response({"error": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)
        
        
class MyTokenObtainPairView(TokenObtainPairView):
    """
    This endpoint takes a username(or email) and password and returns an access and a refresh JSON web token pair.
    """

    serializer_class = MyTokenObtainPairSerializer


class RequestResetPasswordAPIView(APIView):
    """
    This endpoint allows users to request a password reset link via email.
    """
    permission_classes = [AllowAny]
    serializer_class = RequestResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            user = User.objects.get(email_address=email)
            send_mail_data = reset_password_mail(user)
            Util.send_email(send_mail_data)
            return Response({"message": "Password reset email sent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckResetPasswordTokenAPIView(APIView):
    """
    This endpoint checks the validity of a password reset token.
    """
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "The reset link is invalid."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "The reset link is invalid."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "The reset link is valid."}, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    """
    Reset the user's password using a validated token and new password.
    """
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class RetrieveUserProfileAPIView(APIView):
    """
    Retrieve the authenticated user's profile information.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserProfileAPIView(APIView):
    """
    Update the authenticated user's profile details.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ChangePasswordAPIView(APIView):
    """
    This endpoint allows authenticated users to change their password.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get("old_password")

            if not user.check_password(old_password):
                return Response({"old_password": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)