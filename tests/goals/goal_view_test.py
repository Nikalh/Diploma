import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestGoalRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, goal_category__board):
        self.url = self.get_url(goal_pk=goal_category__board.id)

    @staticmethod
    def get_url(goal_pk: int) -> str:
        return reverse('todolist.goals:goal', kwargs={'pk': goal_pk})

    def test_auth_required(self, client):
        """"
        Тест на проверку аутентификации пользователя, неавторизованный пользователь не может просматривать цели
        """
        res = client.get(self.url)
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_retrieve_deleted_goal(self, auth_client, goal):
        """"
        Тест на проверку просмотра удаленной цели
        """
        goal.status = 4
        goal.save()
        res = auth_client.get(self.url)
        assert res.status_code == status.HTTP_404_NOT_FOUND
