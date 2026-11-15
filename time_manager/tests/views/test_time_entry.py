from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from time_manager.tests.factories import TimeEntryFactory

pytestmark = pytest.mark.django_db


def test_time_entry_index_show_time_entries(client, user):
    client.force_login(user)
    time_entry = TimeEntryFactory(user=user)

    response = client.get(reverse("time_manager:time_entry_index"))

    html = response.content.decode()
    assert response.status_code == 200
    assert time_entry.category.name in html


def test_time_entry_index_shows_only_current_user_entry(client, user):
    client.force_login(user)
    time_entry = TimeEntryFactory(user=user)
    other_user_time_entry = TimeEntryFactory()

    response = client.get(reverse("time_manager:time_entry_index"))

    html = response.content.decode()
    assert response.status_code == 200
    assert time_entry.category.name in html
    assert other_user_time_entry.category.name not in html


def test_time_entry_index_orders_newest_first(client, user):
    client.force_login(user)
    older = TimeEntryFactory(user=user, started_at=timezone.now(), ended_at=timezone.now())
    next_time = timezone.now() + timedelta(hours=2)
    newer = TimeEntryFactory(user=user, started_at=next_time, ended_at=next_time)

    response = client.get(reverse("time_manager:time_entry_index"))

    assert list(response.context["time_entries"]) == [newer, older]


def test_time_entry_index_marks_running_entry(client, user):
    client.force_login(user)
    time_entry = TimeEntryFactory(user=user, running=True)

    response = client.get(reverse("time_manager:time_entry_index"))

    assert list(response.context["time_entries"]) == [time_entry]
    html = response.content.decode()
    assert '<span class="badge badge-success animate-pulse">Trwa</span>' in html


def test_time_entry_index_not_showing_badge_when_no_tuning_timers(client, user):
    client.force_login(user)
    time_entry = TimeEntryFactory(user=user)

    response = client.get(reverse("time_manager:time_entry_index"))

    assert list(response.context["time_entries"]) == [time_entry]
    html = response.content.decode()
    assert '<span class="badge badge-success animate-pulse">Trwa</span>' not in html
