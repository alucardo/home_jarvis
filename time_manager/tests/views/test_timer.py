import pytest
from django.urls import reverse

from time_manager.models import TimeEntry
from time_manager.tests.factories import CategoryFactory, TimeEntryFactory

pytestmark = pytest.mark.django_db


def test_timer_start_creates_new_entry_and_redirects(client, user, category):
    client.force_login(user)
    response = client.post(reverse("time_manager:timer_start"), {"category": category.id})

    assert response.status_code == 302
    assert response.url == reverse("dashboard:dashboard")
    time_entry = TimeEntry.objects.get(user=user)
    assert time_entry.category == category
    assert time_entry.ended_at is None


def test_timer_start_with_other_users_category_creates_no_entry(client, user):
    other_user_category = CategoryFactory()
    client.force_login(user)

    response = client.post(reverse("time_manager:timer_start"), {"category": other_user_category.id})

    assert response.status_code == 302
    assert response.url == reverse("dashboard:dashboard")
    assert TimeEntry.objects.count() == 0


def test_timer_start_when_running_not_starting_second(client, user, category):
    client.force_login(user)
    started_time_entry = TimeEntryFactory(user=user, category=category, running=True)

    response = client.post(reverse("time_manager:timer_start"), {"category": category.id})

    assert response.status_code == 302
    assert response.url == reverse("dashboard:dashboard")
    assert TimeEntry.objects.get(user=user) == started_time_entry


def test_timer_stop_finishes_running_entry(client, user):
    time_entry = TimeEntryFactory(user=user, running=True)
    client.force_login(user)

    response = client.post(reverse("time_manager:timer_stop"))

    assert response.status_code == 302
    assert response.url == reverse("dashboard:dashboard")
    time_entry.refresh_from_db()
    assert time_entry.ended_at is not None


def test_timer_stop_for_not_running_timer_redirect_without_error(client, user):
    client.force_login(user)

    response = client.post(reverse("time_manager:timer_stop"))

    assert response.status_code == 302
    assert response.url == reverse("dashboard:dashboard")
    assert not TimeEntry.objects.exists()
