from typing import Callable

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture()
def goal_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db
class TestGoalCreateView:
    url = reverse('todolist.goals:create-goal')

    def test_auth_required(self, client, goal_create_data):
        """"
        Тест на проверку аутентификации пользователя, неавторизованный пользователь получит ошибку авторизации
        """
        res = client.post(self.url, data=goal_create_data())
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_to_create_goal(self, auth_client, goal_create_data, board, goal_category):
        """"Проверка на создание цели со статусом по умолчанию"""
        res = auth_client.post(self.url,
                               data=goal_create_data(category=goal_category.id, board=board, is_deleted=False))
        assert res.status_code == status.HTTP_201_CREATED
        assert res.json()['status'] == 1
