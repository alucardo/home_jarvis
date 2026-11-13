import pytest

from time_manager.exceptions.timer_exceptions import TimerAlreadyRunningError
from time_manager.services.timer_service import start_timer


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