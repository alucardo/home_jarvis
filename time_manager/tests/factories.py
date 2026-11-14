from datetime import timedelta

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from time_manager.models import Category, TimeEntry


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Category {n}")


class TimeEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TimeEntry

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory, user=factory.SelfAttribute("..user"))
    started_at = factory.LazyFunction(lambda: timezone.now() - timedelta(hours=1))
    ended_at = factory.LazyAttribute(lambda entry: entry.started_at + timedelta(hours=1))

    class Params:
        running = factory.Trait(ended_at=None)
