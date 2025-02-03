from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer

class ReadNotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """
        Mark a notification as read.
        """
        return Response({"message": "Notification marked as read."}, status=status.HTTP_200_OK)


class DeleteNotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        Delete a notification.
        """
        return Response({"message": "Notification deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
