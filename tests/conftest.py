from pytest_factoryboy import register

from tests.factories import *

pytest_plugins = 'tests.fixtures'

register(GoalFactory)
register(GoalCategoryFactory)
register(UserFactory)
register(GoalCommentFactory)
register(BoardFactory)
register(BoardParticipantFactory)
