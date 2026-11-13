import pytest
from django.contrib.auth import get_user_model

from time_manager.models import Category


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(email="a@example.com", username="a", password="pass123")

@pytest.fixture
def other_user(db):
    User = get_user_model()
    return User.objects.create_user(email="b@example.com", username="b", password="pass123")

@pytest.fixture
def category(user):
    return Category.objects.create(user=user, name="work")