from enum import Enum

import requests
from django.conf import settings

from todolist.bot.tg.schemas import GetUpdatesResponse, SendMessageResponse


class Command(str, Enum):
    """ Создаем команды для клиента"""
    GET_UPDATES = 'getUpdates'
    SEND_MESSAGE = 'sendMessage'


class TgClient:
    """ Создаем клиент и его функционал:
        _get - получаем команду и отправляем запрос с параметрами, проверяем ответ, возвращаем данные
        get_url -получаем url
        get_updates - получаем обновления
        send_message - отправляем сообщения в чат
    """
    def __init__(self, token: str | None = None):
        self.token = token if token else settings.BOT_TOKEN

    def get_url(self, method: str) -> str:
        # получаем url
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        # обновляем данные
        data = self._get(Command.GET_UPDATES, offset=offset, timeout=timeout)
        return GetUpdatesResponse(**data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        # отправляем сообщение
        data = self._get(Command.SEND_MESSAGE, chat_id=chat_id, text=text)
        return SendMessageResponse(**data)

    def _get(self, command: Command, **params) -> dict:
        url = self.get_url(command)
        response = requests.get(url, params=params)
        if not response.ok:
            print(response.json())
            raise ValueError
        return response.json()
