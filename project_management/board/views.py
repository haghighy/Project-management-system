from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Board, BoardMember, BoardLabel
from .serializers import BoardSerializer, BoardLabelSerializer, BoardMemberSerializer


class CreateBoardAPIView(APIView):
    """
    Create a new board.
    """
    # permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Ensure that the member_creator is set to the current logged-in user
            serializer.save(member_creator=request.user)
            return Response({"message": "Board created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeBoardAPIView(APIView):
    """
    Change details of an existing board.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer

    def put(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs["board_id"], member_creator=request.user)
        serializer = self.serializer_class(board, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Board updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddMemberToBoardAPIView(APIView):
    """
    Add a new member to a board.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BoardMemberSerializer

    def post(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs["board_id"])
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(board=board)
            return Response({"message": "Member added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveMemberFromBoardAPIView(APIView):
    """
    Remove a member from a board.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs["board_id"])
        member = BoardMember.objects.get(board=board, member=request.user)
        member.delete()
        return Response({"message": "Member removed successfully."}, status=status.HTTP_204_NO_CONTENT)


class ChangeMemberTypeAPIView(APIView):
    """
    Change a member's role on a board.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BoardMemberSerializer

    def put(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs["board_id"])
        member = BoardMember.objects.get(board=board, member=request.user)
        member.member_type = request.data.get("member_type")
        member.save()
        return Response({"message": "Member type updated successfully."}, status=status.HTTP_200_OK)


class ChangeBoardVisibilityAPIView(APIView):
    """
    Change a board's visibility to public or private.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer

    def put(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs["board_id"])
        board.is_public = request.data.get("is_public")
        board.save()
        return Response({"message": "Board visibility updated successfully."}, status=status.HTTP_200_OK)


class CloseBoardAPIView(APIView):
    """
    Close a board.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs["board_id"])
        board.is_closed = True
        board.save()
        return Response({"message": "Board closed successfully."}, status=status.HTTP_200_OK)


class DeleteClosedBoardAPIView(APIView):
    """
    Delete a closed board.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs["board_id"], is_closed=True)
        board.delete()
        return Response({"message": "Board deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class CreateShareLinkAPIView(APIView):
    """
    Create a share link for a board.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs["board_id"])
        board.board_shared_link = request.data.get("shared_link")
        board.save()
        return Response({"message": "Share link created successfully."}, status=status.HTTP_201_CREATED)


class RemoveShareLinkAPIView(APIView):
    """
    Remove the share link for a board.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs["board_id"])
        board.board_shared_link = None
        board.save()
        return Response({"message": "Share link removed successfully."}, status=status.HTTP_204_NO_CONTENT)


class AddBoardLabelAPIView(APIView):
    """
    Add a label to a board.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs["board_id"])
        label_serializer = BoardLabelSerializer(data=request.data)
        if label_serializer.is_valid():
            label_serializer.save(board=board)
            return Response({"message": "Board label added successfully."}, status=status.HTTP_201_CREATED)
        return Response(label_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveBoardLabelAPIView(APIView):
    """
    Remove a label from a board.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        board = Board.objects.get(id=kwargs["board_id"])
        label = BoardLabel.objects.get(id=kwargs["label_id"], board=board)
        label.delete()
        return Response({"message": "Board label removed successfully."}, status=status.HTTP_204_NO_CONTENT)
