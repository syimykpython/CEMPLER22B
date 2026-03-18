import requests
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.serializers import OauthCodeSerializer

User = get_user_model()

class GoogleLoginAPIView(APIView):
    def post(self, request):
        serializer = OauthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        # Получаем access token
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
        )

        token_json = token_response.json()
        access_token = token_json.get("access_token")
        if not access_token:
            return Response({"error": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем данные пользователя
        user_response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_response.json()
        email = user_data.get("email")
        first_name = user_data.get("given_name")
        last_name = user_data.get("family_name")

        if not email:
            return Response({"error": "Email not provided by Google"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем или обновляем пользователя
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "registration_source": "google",
                "is_active": True,
            }
        )
        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = True

        user.last_login = timezone.now()
        user.save()

        # Возвращаем токен
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })