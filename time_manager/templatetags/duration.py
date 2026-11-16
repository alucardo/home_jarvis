from django import template

register = template.Library()


@register.filter
def duration(value):
    seconds = value.total_seconds()
    if 0 < seconds < 60:
        seconds = 60
    hours, remainder = divmod(int(seconds), 3600)
    minutes = remainder // 60
    return f"{hours:02d}:{minutes:02d}"
