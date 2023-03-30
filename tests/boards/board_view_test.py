import pytest
from django.urls import reverse
from rest_framework import status

from todolist.goals.models import BoardParticipant


@pytest.mark.django_db
class TestBoardRetrieveView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int) -> str:
        return reverse('todolist.goals:board', kwargs={'pk': board_pk})

    def test_auth_required(self, client):
        """"
        Тест на проверку аутентификации пользователя, неавторизованный пользователь не может просматривать доски
        """
        res = client.get(self.url)
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_retrieve_deleted_board(self, auth_client, board):
        """"
        Тест на проверку просмотра удаленной доски
        """
        board.is_deleted = True
        board.save()
        res = auth_client.get(self.url)
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_failed_to_retrieve_foreign_board(self, client, user_factory):
        """"
        Тест на проверку просмотра доски в которой пользователь не является участником
        """
        another_user = user_factory.create()
        client.force_login(another_user)
        res = client.get(self.url)
        assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestBoardDestroyView:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int) -> str:
        return reverse('todolist.goals:board', kwargs={'pk': board_pk})

    def test_auth_required(self, client):
        """"
        Тест на проверку аутентификации пользователя, неавторизованный пользователь не может просматривать доски
        """
        res = client.get(self.url)
        assert res.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('role', [BoardParticipant.Role.writer, BoardParticipant.Role.reader],
                             ids=['writer', 'reader'])
    def test_not_owner_failed_to_deleted_board(self, client, user_factory, board, board_participant_factory, role):
        """"
        Тест на проверку аутентификации пользователя, неавторизованный пользователь не может удалять доски
        """
        another_user = user_factory.create()
        board_participant_factory.create(user=another_user, board=board, role=role)
        client.force_login(another_user)
        res = client.delete(self.url)
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_can_to_deleted_board(self, auth_client, board):
        """"
        Тест на проверку, что пользователь с ролью владельца может удалять доски
        """

        res = auth_client.delete(self.url)
        assert res.status_code == status.HTTP_204_NO_CONTENT
        board.refresh_from_db()
        assert board.is_deleted is True
