import pytest
from django.db import IntegrityError

from time_manager.models import Category

pytestmark = pytest.mark.django_db

def test_category_uniq_name_per_user(user):
    name = "work"
    Category.objects.create(name=name, user=user)
    with pytest.raises(IntegrityError):
        Category.objects.create(name=name, user=user)


def test_category_same_name_diff_user(user, other_user):
    name = "work"
    Category.objects.create(name=name, user=user)
    Category.objects.create(name=name, user=other_user)
    assert Category.objects.filter(name=name).count() == 2