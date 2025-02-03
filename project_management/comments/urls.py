from django.urls import path
from . import views

urlpatterns = [
    path('add-comment/', views.AddCommentToCardAPIView.as_view(), name='add-comment-to-card'),
    path('show-comments/<uuid:card_id>/', views.ShowCommentsOnCardAPIView.as_view(), name='show-comments-on-card'),
]
