from datetime import timedelta

import pytest
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone

from tests.helpers import message_levels
from time_manager.models import TimeEntry
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


def test_time_entry_delete_when_get_request_gets_405(client, user):
    client.force_login(user)
    time_entry = TimeEntryFactory(user=user)

    response = client.get(reverse("time_manager:time_entry_delete", kwargs={"pk": time_entry.id}))

    assert response.status_code == 405


def test_time_entry_delete_when_correct_removes_and_redirect_user(client, user):
    client.force_login(user)
    time_entry = TimeEntryFactory(user=user)

    response = client.post(reverse("time_manager:time_entry_delete", kwargs={"pk": time_entry.id}))

    assert response.status_code == 302
    assert response.url == reverse("time_manager:time_entry_index")
    assert not TimeEntry.objects.filter(id=time_entry.id).exists()


def test_time_entry_delete_when_removing_not_existing_returns_404(client, user):
    time_entry = TimeEntryFactory(user=user)
    time_entry_id = time_entry.id
    time_entry.delete()
    client.force_login(user)

    response = client.post(reverse("time_manager:time_entry_delete", kwargs={"pk": time_entry_id}))

    assert response.status_code == 404


def test_time_entry_delete_when_removing_not_users_returns_404(client, user, other_user):
    time_entry = TimeEntryFactory(user=user)
    client.force_login(other_user)

    response = client.post(reverse("time_manager:time_entry_delete", kwargs={"pk": time_entry.id}))

    assert response.status_code == 404
    assert TimeEntry.objects.filter(id=time_entry.id).exists()


def test_time_entry_delete_when_running_timer_blocks_removing(client, user):
    time_entry = TimeEntryFactory(user=user, running=True)
    client.force_login(user)

    response = client.post(reverse("time_manager:time_entry_delete", kwargs={"pk": time_entry.id}))

    assert response.status_code == 302
    assert response.url == reverse("time_manager:time_entry_index")
    assert TimeEntry.objects.filter(id=time_entry.id).exists()
    assert message_levels(response) == [messages.ERROR]
