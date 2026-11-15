from django.contrib.messages import get_messages


def message_levels(response):
    return [message.level for message in get_messages(response.wsgi_request)]
