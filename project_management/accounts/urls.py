from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    # register
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("email-activation/<uidb64>/<token>/", views.ActivateEmailAPIView.as_view(), name="email-activation"),
    #login
    path("login/", views.MyTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]