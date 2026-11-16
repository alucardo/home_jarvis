from datetime import timedelta

import pytest

from time_manager.templatetags.duration import duration


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (timedelta(0), "00:00"),
        (timedelta(seconds=20), "00:01"),
        (timedelta(minutes=25), "00:25"),
        (timedelta(hours=1, minutes=30), "01:30"),
        (timedelta(hours=26, minutes=5), "26:05"),
    ],
)
def test_duration_filter(value, expected):
    assert duration(value) == expected
