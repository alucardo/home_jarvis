import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta

from time_manager.models import Category, TimeEntry

@pytest.mark.django_db
def test_time_entry_saves_for_category_owner(user, category):
    entry = TimeEntry.objects.create(
        user=user,
        category=category,
        started_at=timezone.now(),
    )
    assert entry.pk is not None
    assert entry.ended_at is None


@pytest.mark.django_db
def test_user_and_category_user_constraint(other_user, category):
    with pytest.raises(ValidationError):
        TimeEntry.objects.create(
            started_at=timezone.now(),
            user=other_user,
            category=category
        )

@pytest.mark.django_db
def test_started_at_before_ended_at(user, category):
    with pytest.raises(ValidationError):
        TimeEntry.objects.create(
            started_at=timezone.now(),
            ended_at=timezone.now() - timedelta(hours=1),
            user=user,
            category=category
        )

@pytest.mark.django_db
def test_user_can_have_running_and_finished_entries(user, category):
    old_entry = TimeEntry.objects.create(
        started_at=timezone.now() - timedelta(hours=1),
        ended_at=timezone.now(),
        user=user,
        category=category
    )

    entry = TimeEntry.objects.create(
        started_at=timezone.now(),
        user=user,
        category=category
    )

    assert old_entry.pk is not None
    assert entry.pk is not None


@pytest.mark.django_db
def test_user_can_have_only_one_running_entry(user, category):
    TimeEntry.objects.create(
        started_at=timezone.now(),
        user=user,
        category=category
    )
    with pytest.raises(ValidationError):
        TimeEntry.objects.create(
            started_at=timezone.now(),
            user=user,
            category=category
        )

@pytest.mark.django_db
def test_many_users_can_have_running_entries(user, other_user, category):
    other_user_category = Category.objects.create(user=other_user, name="work")
    user_entry = TimeEntry.objects.create(
        started_at=timezone.now(),
        user=user,
        category=category
    )

    other_user_entry = TimeEntry.objects.create(
        started_at=timezone.now(),
        user=other_user,
        category=other_user_category
    )

    assert user_entry.pk is not None
    assert other_user_entry.pk is not None

@pytest.mark.django_db
def test_db_rejects_second_running_entry_per_user(user, category):
    TimeEntry.objects.create(
        started_at=timezone.now(),
        user=user,
        category=category,
    )
    with pytest.raises(IntegrityError):
        TimeEntry.objects.bulk_create([
            TimeEntry(
                started_at=timezone.now(),
                user=user,
                category=category,
            )
        ])