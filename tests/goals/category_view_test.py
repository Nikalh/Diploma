import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestGoalCategoryRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, goal_category__board):
        self.url = self.get_url(category_pk=goal_category__board.id)

    @staticmethod
    def get_url(category_pk: int) -> str:
        return reverse('todolist.goals:category', kwargs={'pk': category_pk})

    def test_auth_required(self, client):
        """"
        Тест на проверку аутентификации пользователя, неавторизованный пользователь не может просматривать категории
        """
        res = client.get(self.url)
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_retrieve_deleted_category(self, auth_client, goal__category):
        """"
        Тест на проверку просмотра удаленной категории
        """
        goal__category.is_deleted = True
        goal__category.save()
        res = auth_client.get(self.url)
        assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_list_category(auth_client):
    """"
    Тест на получение списка категорий
    """
    url = reverse('todolist.goals:category-list')
    res = auth_client.get(url)
    assert res.status_code == status.HTTP_200_OK
