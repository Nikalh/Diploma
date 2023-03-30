import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProfileView:
    url = reverse('todolist.core:profile')

    def test_auth_required(self, client):
        """"
        Тест на проверку аутентификации пользователя, неавторизованный пользователь не имеет доступа
        """
        res = client.get(self.url)
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_user_logout(self, auth_client):
        """"
        Тест на проверку выхода пользователя
        """
        res = auth_client.delete(self.url)
        assert res.status_code == status.HTTP_204_NO_CONTENT

    def test_update_password(self, auth_client):
        """"
        Тест на обновление пароля пользователя
        """
        password = 'new_password'
        res = auth_client.patch(self.url, password=password)
        assert res.status_code == status.HTTP_200_OK
