from typing import Any

from django.contrib.auth import login, logout
from django.db.models import QuerySet
from rest_framework import generics, permissions
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from todolist.core.models import User
from todolist.core.serializers import CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer


class SingUpView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request=request, user=serializer.save())
        return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class: Serializer = ProfileSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance: User):
        logout(self.request)


class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class: Serializer = UpdatePasswordSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
