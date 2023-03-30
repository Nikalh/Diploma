from typing import Any

from django.contrib.auth import login, logout
from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from todolist.core.models import User
from todolist.core.serializers import CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer


class SingUpView(generics.CreateAPIView):
    """ Создаем вью регистрации пользователя"""
    serializer_class = CreateUserSerializer


class LoginView(generics.CreateAPIView):
    """ Создаем вью входа пользователя"""
    serializer_class = LoginSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        # реализовываем вход пользователя
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request=request, user=serializer.save())
        return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """ Создаем вью получения, обновления и удаления профиля"""
    serializer_class: Serializer = ProfileSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)

    def get_object(self):
        # получаем профиль пользователя
        return self.request.user

    def perform_destroy(self, instance: User):
        # реализовываем выход пользователя
        logout(self.request)


class UpdatePasswordView(generics.UpdateAPIView):
    """ Создаем вью обновления пароля"""
    serializer_class: Serializer = UpdatePasswordSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
