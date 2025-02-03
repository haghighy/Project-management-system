from django.urls import path

from . import views

urlpatterns = [
    # register
    path("register/", views.RegisterAPIView.as_view(), name="register"),
]