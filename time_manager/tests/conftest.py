import pytest

from time_manager.tests.factories import CategoryFactory, UserFactory


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def other_user(db):
    return UserFactory()


@pytest.fixture
def category(user):
    return CategoryFactory(user=user)
