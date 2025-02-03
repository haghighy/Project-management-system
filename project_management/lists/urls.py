from django.urls import path
from . import views

urlpatterns = [
    # Add a list to a board
    path('add-list/', views.AddListToBoardAPIView.as_view(), name='add-list-to-board'),

    # Delete a list from a board
    path('delete-list/<uuid:list_id>/', views.DeleteListFromBoardAPIView.as_view(), name='delete-list-from-board'),

    # Change a list’s position
    path('change-list-position/<uuid:list_id>/', views.ChangeListPositionAPIView.as_view(), name='change-list-position'),

    # Change a list
    path('change-list/<uuid:list_id>/', views.ChangeListAPIView.as_view(), name='change-list'),

    # Close a list
    path('close-list/<uuid:list_id>/', views.CloseListAPIView.as_view(), name='close-list'),
]
