from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from django.db import transaction
import random
import string

from .models import User, ConfirmationCode
from .serializers import RegisterSerializer, LoginSerializer, ConfirmationSerializer


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = serializer.save()
            code = ''.join(random.choices(string.digits, k=6))
            ConfirmationCode.objects.create(user=user, code=code)

        return Response(
            {"user_id": user.id, "confirmation_code": code},
            status=status.HTTP_201_CREATED
        )


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"key": token.key})


class ConfirmUserAPIView(APIView):
    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        with transaction.atomic():
            user.is_active = True
            user.save()
            Token.objects.get_or_create(user=user)
            ConfirmationCode.objects.filter(user=user).delete()

        token = Token.objects.get(user=user)
        return Response(
            {"message": "Аккаунт активирован", "key": token.key},
            status=status.HTTP_200_OK
        )