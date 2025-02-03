from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import UserRegisterSerializer, UserSerializerWithToken


class RegisterAPIView(APIView):
    """
    This endpoint allows clients to register a new user by providing an email, and password.
    """
    
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    
    def post(self, request, *args, **kwargs):
        return Response({"message": "The User Registered Successfully."}, status=status.HTTP_201_CREATED)
    
    
class ActivateEmailAPIView(APIView):
    """
    Activates a user account if the provided token is valid.
    """

    permission_classes = [AllowAny]
    serializer_class = UserSerializerWithToken