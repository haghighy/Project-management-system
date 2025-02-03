from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateBoardAPIView.as_view(), name='create-board'),
    path('change/<str:board_id>/', views.ChangeBoardAPIView.as_view(), name='change-board'),
    path('add-member/<str:board_id>/', views.AddMemberToBoardAPIView.as_view(), name='add-member'),
    path('remove-member/<str:board_id>/', views.RemoveMemberFromBoardAPIView.as_view(), name='remove-member'),
    path('change-member-type/<str:board_id>/', views.ChangeMemberTypeAPIView.as_view(), name='change-member-type'),
    path('change-visibility/<str:board_id>/', views.ChangeBoardVisibilityAPIView.as_view(), name='change-board-visibility'),
    path('close/<str:board_id>/', views.CloseBoardAPIView.as_view(), name='close-board'),
    path('delete-closed/<str:board_id>/', views.DeleteClosedBoardAPIView.as_view(), name='delete-closed-board'),
    path('create-share-link/<str:board_id>/', views.CreateShareLinkAPIView.as_view(), name='create-share-link'),
    path('remove-share-link/<str:board_id>/', views.RemoveShareLinkAPIView.as_view(), name='remove-share-link'),
    path('add-label/', views.AddBoardLabelAPIView.as_view(), name='add-board-label'),
    path('remove-label/<str:board_id>/<int:label_id>/', views.RemoveBoardLabelAPIView.as_view(), name='remove-board-label'),
]
