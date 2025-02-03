from django.urls import path

from . import views

urlpatterns = [
    # register
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("email-activation/<uidb64>/<token>/", views.ActivateEmailAPIView.as_view(), name="email-activation"),
]