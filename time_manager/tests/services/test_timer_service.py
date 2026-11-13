import pytest

from time_manager.exceptions.timer_exceptions import TimerAlreadyRunningError, TimerNotRunningError
from time_manager.services.timer_service import start_timer, stop_timer


@pytest.mark.django_db
def test_start_timer_creates_time_entry(user, category):
    timer = start_timer(user, category)

    assert timer.user_id == user.id
    assert timer.category_id == category.id
    assert timer.started_at is not None
    assert timer.ended_at is None


@pytest.mark.django_db
def test_user_can_have_only_one_running_timer(user, category):
    start_timer(user, category)

    with pytest.raises(TimerAlreadyRunningError):
        start_timer(user, category)


@pytest.mark.django_db
def test_service_stopping_time_entry(user, category):
    start_timer(user, category)
    timer = stop_timer(user)
    timer.refresh_from_db()
    assert timer.ended_at is not None


@pytest.mark.django_db
def test_stop_timer_returns_error_if_timer_is_not_running(user, category):
    start_timer(user, category)
    stop_timer(user)
    with pytest.raises(TimerNotRunningError):
        stop_timer(user)
