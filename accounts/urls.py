from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

app_name = "accounts"

urlpatterns = [
    path("signup/", views.AccountAPIView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("password/", views.create_password, name="password"),
    path("profiles/<int:user_id>/", views.AccountDetailAPIView.as_view(), name=""),
]
