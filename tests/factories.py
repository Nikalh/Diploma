import factory
from django.utils import timezone

from todolist.core.models import User
from todolist.goals.models import Goal, GoalCategory, GoalComment, Board, BoardParticipant


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return User.objects.create_user(*args, **kwargs)


class DatesFactoryMixin(factory.django.DjangoModelFactory):
    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)

    class Meta:
        abstract = True


class BoardFactory(DatesFactoryMixin):
    class Meta:
        model = Board

    title = factory.Faker('sentence')

    # Создаем доску, принадлежащую какому-то пользователю
    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)


class BoardParticipantFactory(DatesFactoryMixin):
    class Meta:
        model = BoardParticipant

    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)
    is_deleted = 'False'


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.Faker('sentence')
    category = factory.SubFactory(GoalCategoryFactory)
    user = factory.SubFactory(UserFactory)


class GoalCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text = factory.Faker('sentence')
    goal = factory.SubFactory(GoalFactory)
    user = factory.SubFactory(UserFactory)
