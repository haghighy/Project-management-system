from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Card, CardLabel, CardMember, CardAction
from .serializers import CardSerializer, CardLabelSerializer, CardMemberSerializer, CardActionSerializer

class AddCardToListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Structure to add a card to a list
        return Response({"message": "Card added to list."}, status=status.HTTP_201_CREATED)


class RemoveCardFromListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        # Structure to remove a card from a list
        return Response({"message": "Card removed from list."}, status=status.HTTP_204_NO_CONTENT)


class ChangeCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # Structure to change a card's details
        return Response({"message": "Card updated successfully."}, status=status.HTTP_200_OK)


class ChangeCardPositionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # Structure to change a card's position
        return Response({"message": "Card position updated."}, status=status.HTTP_200_OK)


class AddDueToCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # Structure to add due date to card
        return Response({"message": "Due date added to card."}, status=status.HTTP_200_OK)


class AddDueReminderToCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        # Structure to add due reminder to card
        return Response({"message": "Due reminder added to card."}, status=status.HTTP_200_OK)


class AddLabelToCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Structure to add a label to a card
        return Response({"message": "Label added to card."}, status=status.HTTP_201_CREATED)


class RemoveLabelFromCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        # Structure to remove a label from a card
        return Response({"message": "Label removed from card."}, status=status.HTTP_204_NO_CONTENT)


class AddMemberToCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Structure to add a member to a card
        return Response({"message": "Member added to card."}, status=status.HTTP_201_CREATED)


class RemoveMemberFromCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        # Structure to remove a member from a card
        return Response({"message": "Member removed from card."}, status=status.HTTP_204_NO_CONTENT)


class AddAttachmentToCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Structure to add an attachment to a card
        return Response({"message": "Attachment added to card."}, status=status.HTTP_201_CREATED)


class RemoveAttachmentFromCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        # Structure to remove an attachment from a card
        return Response({"message": "Attachment removed from card."}, status=status.HTTP_204_NO_CONTENT)
