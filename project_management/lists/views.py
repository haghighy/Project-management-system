from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import List
from .serializers import ListSerializer

class AddListToBoardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Add a new list to a board.
        """
        # Add list to board logic
        return Response({"message": "List added to board."}, status=status.HTTP_201_CREATED)


class DeleteListFromBoardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """
        Delete a list from a board.
        """
        # Delete list from board logic
        return Response({"message": "List deleted from board."}, status=status.HTTP_204_NO_CONTENT)


class ChangeListPositionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """
        Change the position of a list.
        """
        # Change list position logic
        return Response({"message": "List position updated."}, status=status.HTTP_200_OK)


class ChangeListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """
        Change the details of a list (e.g., name, is_closed).
        """
        # Change list details logic
        return Response({"message": "List details updated."}, status=status.HTTP_200_OK)


class CloseListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """
        Close a list by setting is_closed to True.
        """
        # Close list logic
        return Response({"message": "List closed."}, status=status.HTTP_200_OK)
