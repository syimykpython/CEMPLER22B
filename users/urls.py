from django.urls import path
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import (
    AuthorizationAPIView,
    ConfirmUserAPIView,
    CustomTokenObtainPairView,
    RegistrationAPIView,
)
from users.google_oauth import GoogleLoginAPIView, OauthCodeSerializer

urlpatterns = [
    path("registration/", RegistrationAPIView.as_view()),
    path("authorization/", AuthorizationAPIView.as_view()),
    path("confirm/", ConfirmUserAPIView.as_view()),

    path("api/v1/jwt/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("google-login/", GoogleLoginAPIView.as_view()),
]