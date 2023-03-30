from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from todolist.core.fields import PasswordField
from todolist.core.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """ Создаем сериализатор на создание(регистрация) пользователя с указанием обязательных полей"""
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        # проверяем пароль и его повторный ввод на равенство
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError({'password_repeat': 'Passwords не совпадают'})
        return attrs

    def create(self, validated_data: dict) -> User:
        # переопределяем метод
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """ Создаем сериализатор для входа пользователя с указанием обязательных полей"""
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        read_only_fields = ('id', 'first_name', 'last_name', 'email')

    def create(self, validated_data: dict) -> User:
        # переопределяем метод с проверкой аутентификации пользователя
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if not user:
            raise AuthenticationFailed
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """ Создаем сериализатор на получение профиля пользователя"""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    """ Создаем сериализатор для обновления пароля пользователя с указанием обязательных полей"""
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    def validate_old_password(self, old_password: str) -> str:
        # проверяем старый пароль и его ввод на равенство
        if not self.instance.check_password(old_password):
            raise ValidationError('Password is not correct')
        return old_password

    def update(self, instance: User, validated_data: dict) -> User:
        # обновляем пароль
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
