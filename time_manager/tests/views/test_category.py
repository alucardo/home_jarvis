import pytest
from django.urls import reverse

from time_manager.tests.factories import TimeEntryFactory, CategoryFactory

from time_manager.models import Category, TimeEntry

pytestmark = pytest.mark.django_db


def test_category_index_shows_only_own_categories(client, user, other_user, category):
    CategoryFactory(name="secret", user=other_user)
    client.force_login(user)

    response = client.get(reverse('time_manager:category_index'))

    html = response.content.decode()
    assert response.status_code == 200
    assert category.name in html
    assert "secret" not in html


def test_create_category_get_view_success(client, user):
    client.force_login(user)
    response = client.get(reverse('time_manager:category_create'))

    assert response.status_code == 200


def test_category_create(client, user):
    client.force_login(user)
    response = client.post(reverse('time_manager:category_create'), {'name': 'secret'})

    assert response.status_code == 302
    assert response.url == reverse('time_manager:category_index')
    assert Category.objects.filter(user=user, name='secret').exists()


def test_category_create_reject_empty_name(client, user):
    client.force_login(user)
    response = client.post(reverse('time_manager:category_create'), {'name': ''})

    assert response.status_code == 200
    assert 'name' in response.context['form'].errors
    assert Category.objects.filter(user=user).count() == 0


def test_category_create_rejects_duplicate_name(client, user, category):
    client.force_login(user)

    response = client.post(reverse('time_manager:category_create'), {'name': category.name})

    assert response.status_code == 200
    assert 'name' in response.context['form'].errors
    assert Category.objects.filter(user=user, name=category.name).count() == 1


def test_category_delete_when_correct_removes_and_redirect_user(client, user, category):
    client.force_login(user)

    response = client.post(reverse('time_manager:category_delete', kwargs={'pk': category.id}))

    assert response.status_code == 302
    assert response.url == reverse('time_manager:category_index')
    assert not Category.objects.filter(id=category.id).exists()


def test_category_delete_when_removing_removes_time_entry(client, user, category):
    client.force_login(user)
    time_entry = TimeEntryFactory(user=user, category=category)
    time_entry_form_other_category = TimeEntryFactory(user=user)

    client.post(reverse('time_manager:category_delete', kwargs={'pk': category.id}))

    assert not TimeEntry.objects.filter(id=time_entry.id).exists()
    assert TimeEntry.objects.filter(id=time_entry_form_other_category.id).exists()


def test_category_delete_when_removing_not_existing_returns_404(client, user, category):
    category_id = category.id
    category.delete()
    client.force_login(user)

    response = client.post(reverse('time_manager:category_delete', kwargs={'pk': category_id}))

    assert response.status_code == 404


def test_category_delete_when_removing_not_users_returns_404(client, other_user, category):
    client.force_login(other_user)

    response = client.post(reverse('time_manager:category_delete', kwargs={'pk': category.id}))

    assert response.status_code == 404
    assert Category.objects.filter(id=category.id).exists()


def test_category_delete_when_get_request_gets_405(client, user, category):
    client.force_login(user)

    response = client.get(reverse('time_manager:category_delete', kwargs={'pk': category.id}))

    assert response.status_code == 405
    assert Category.objects.filter(id=category.id).exists()
