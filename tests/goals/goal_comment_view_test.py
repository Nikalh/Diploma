import pytest
from django.urls import reverse
from rest_framework import status

from todolist.goals.models import GoalComment


@pytest.mark.django_db
class TestGoalCommentRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, goal_comment):
        self.url = self.get_url(comment_pk=goal_comment.id)

    @staticmethod
    def get_url(comment_pk: int) -> str:
        return reverse('todolist.goals:comment', kwargs={'pk': comment_pk})

    def test_auth_required(self, client):
        """"
        Тест на проверку аутентификации пользователя, неавторизованный пользователь не может просматривать комментарии
        """
        res = client.get(self.url)
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_get_detail_comment(self, auth_client, user):
        """"
        Тест на проверку получения конкретного комментария
        """

        res = auth_client.get(self.url)

        assert res.status_code == status.HTTP_200_OK
        comment = GoalComment.objects.get(user_id=user.id)
        assert comment.goal_id == res.data['id']


@pytest.mark.django_db
def test_get_list_comment(auth_client):
    """"
    Тест на получение списка комментариев
    """

    url = reverse('todolist.goals:comment-list')

    res = auth_client.get(url)
    assert res.status_code == status.HTTP_200_OK
