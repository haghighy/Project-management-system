from django.urls import path
from . import views

urlpatterns = [
    # Mark a notification as read
    path('read-notification/<uuid:notification_id>/', views.ReadNotificationAPIView.as_view(), name='read-notification'),

    # Delete a notification
    path('delete-notification/<uuid:notification_id>/', views.DeleteNotificationAPIView.as_view(), name='delete-notification'),
]
