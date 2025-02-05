from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    # register
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("email-activation/<uidb64>/<token>/", views.ActivateEmailAPIView.as_view(), name="email-activation"),
    path("send-email-activation/", views.SendActivationEmailAPIView.as_view(), name="send-activation-email"),
    #login
    path("login/", views.MyTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    #reset password
    path('password-reset/request/', views.RequestResetPasswordAPIView.as_view(), name='password_reset_request'),
    path('password-reset/<uidb64>/<token>/', views.CheckResetPasswordTokenAPIView.as_view(), name='password_reset_validate'),
    path('password-reset/confirm/', views.ResetPasswordAPIView.as_view(), name='password_reset_confirm'),
    #profile
    path('profile/', views.RetrieveUserProfileAPIView.as_view(), name='get-profile'),
    path('profile/update/', views.UpdateUserProfileAPIView.as_view(), name='update-profile'),
    #change password
    path('change-password/', views.ChangePasswordAPIView.as_view(), name='change-password'),
    path('change-email/', views.ChangeEmailAPIView.as_view(), name='change-email'),
    # path('confirm-email-change/<uidb64>/<token>/', views.ConfirmEmailChangeAPIView.as_view(), name='confirm-email-change'),
]