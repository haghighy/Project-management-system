from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer

class AddCommentToCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Add a new comment to a card.
        """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(member=request.user)  
            return Response({"message": "Comment added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowCommentsOnCardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Show all comments for a specific card.
        """
        card_id = kwargs.get('card_id')
        comments = Comment.objects.filter(card_id=card_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
