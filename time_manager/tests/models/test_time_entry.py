import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from time_manager.models import Category, TimeEntry

@pytest.mark.django_db
def test_time_entry_saves_for_category_owner(user):
    category = Category.objects.create(user=user, name="work")
    entry = TimeEntry.objects.create(
        user=user,
        category=category,
        started_at=timezone.now(),
    )
    assert entry.pk is not None
    assert entry.ended_at is None


@pytest.mark.django_db
def test_user_and_category_user_constraint(user, other_user):
    category = Category.objects.create(user=user, name="work")
    with pytest.raises(ValidationError):
        TimeEntry.objects.create(
            started_at=timezone.now(),
            user=other_user,
            category=category
        )

@pytest.mark.django_db
def test_started_at_before_ended_at(user):
    category = Category.objects.create(user=user, name="work")
    with pytest.raises(ValidationError):
        TimeEntry.objects.create(
            started_at=timezone.now(),
            ended_at=timezone.now() - timedelta(hours=1),
            user=user,
            category=category
        )