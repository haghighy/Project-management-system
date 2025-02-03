from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import UserRegisterSerializer
from .utils import activation_mail, Util

User = get_user_model()


class RegisterAPIView(APIView):
    """
    This endpoint allows clients to register a new user and sends 
    an activation email.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        
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
                user.save()
                return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)

            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except (User.DoesNotExist, ValueError):
            return Response({"error": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)