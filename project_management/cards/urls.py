from django.urls import path
from . import views

urlpatterns = [
    # Add a card to a list
    path('add-card-to-list/', views.AddCardToListAPIView.as_view(), name='add-card-to-list'),

    # Remove a card from a list
    path('remove-card-from-list/<uuid:card_id>/', views.RemoveCardFromListAPIView.as_view(), name='remove-card-from-list'),

    # Change a card
    path('change-card/<uuid:card_id>/', views.ChangeCardAPIView.as_view(), name='change-card'),

    # Change a card’s position
    path('change-card-position/<uuid:card_id>/', views.ChangeCardPositionAPIView.as_view(), name='change-card-position'),

    # Add due to a card
    path('add-due-to-card/<uuid:card_id>/', views.AddDueToCardAPIView.as_view(), name='add-due-to-card'),

    # Add due reminder to a card
    path('add-due-reminder-to-card/<uuid:card_id>/', views.AddDueReminderToCardAPIView.as_view(), name='add-due-reminder-to-card'),

    # Add a label to a card
    path('add-label-to-card/<uuid:card_id>/', views.AddLabelToCardAPIView.as_view(), name='add-label-to-card'),

    # Remove a label from a card
    path('remove-label-from-card/<uuid:card_id>/<uuid:label_id>/', views.RemoveLabelFromCardAPIView.as_view(), name='remove-label-from-card'),

    # Add a member to a card
    path('add-member-to-card/<uuid:card_id>/', views.AddMemberToCardAPIView.as_view(), name='add-member-to-card'),

    # Remove a member from a card
    path('remove-member-from-card/<uuid:card_id>/<uuid:member_id>/', views.RemoveMemberFromCardAPIView.as_view(), name='remove-member-from-card'),

    # Add an attachment to a card
    path('add-attachment-to-card/<uuid:card_id>/', views.AddAttachmentToCardAPIView.as_view(), name='add-attachment-to-card'),

    # Remove an attachment from a card
    path('remove-attachment-from-card/<uuid:card_id>/<uuid:attachment_id>/', views.RemoveAttachmentFromCardAPIView.as_view(), name='remove-attachment-from-card'),
]
