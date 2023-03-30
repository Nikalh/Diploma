from typing import Callable
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture()
def category_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db
class TestGoalCategoryCreateView:
    url = reverse('todolist.goals:create-category')

    def test_auth_required(self, client, category_create_data):
        """"
        Тест на проверку аутентификации пользователя, неавторизованный пользователь получит ошибку авторизации
        """
        res = client.post(self.url, data=category_create_data())
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_create_category(self, auth_client, category_create_data, board):
        """Проверка на создание категории"""
        res = auth_client.post(self.url, data=category_create_data(is_deleted=False, board=board.pk))
        assert res.status_code == status.HTTP_201_CREATED
