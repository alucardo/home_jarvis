from django.utils import timezone

from time_manager.exceptions.timer_exceptions import TimerAlreadyRunningError
from time_manager.models import TimeEntry


def start_timer(user, category):
    if TimeEntry.objects.filter(user=user, ended_at__isnull=True).exists():
        raise TimerAlreadyRunningError("Timer already running")

    time_entry = TimeEntry.objects.create(
        user=user,
        started_at=timezone.now(),
        category=category,
    )
    return time_entry