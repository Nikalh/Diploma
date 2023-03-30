from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from todolist.bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    """ Создаем сериализатор телеграмм пользователя"""
    tg_id = serializers.SlugField(source='chat_id', read_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_id', 'verification_code', 'user_id')
        read_only_fields = ('tg_id', 'user_id')

    def validate_verification_code(self, code: str) -> str:
        # проверяем верификационный код
        try:
            self.tg_user = TgUser.objects.get(verification_code=code)
        except TgUser.DoesNotExist:
            raise ValidationError('Field is incorrect')
        return code

    def update(self, instance: TgUser, validated_data: dict):
        # обновляем данные телеграмм пользователя
        return self.tg_user
