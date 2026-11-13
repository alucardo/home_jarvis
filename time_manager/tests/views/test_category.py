import pytest
from django.urls import reverse

from time_manager.models import Category


@pytest.mark.django_db
def test_category_index_shows_only_own_categories(client, user, other_user, category):
    Category.objects.create(user=other_user, name="secret")
    client.force_login(user)

    response = client.get(reverse('time_manager:category_index'))

    html = response.content.decode()
    assert response.status_code == 200
    assert category.name in html
    assert "secret" not in html


@pytest.mark.django_db
def test_create_category_get_view_success(client, user):
    client.force_login(user)
    response = client.get(reverse('time_manager:category_create'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_category_create(client, user):
    client.force_login(user)
    response = client.post(reverse('time_manager:category_create'), {'name': 'secret'})

    assert response.status_code == 302
    assert response.url == reverse('time_manager:category_index')
    assert Category.objects.filter(user=user, name='secret').exists()

@pytest.mark.django_db
def test_category_create_reject_empty_name(client, user):
    client.force_login(user)
    response = client.post(reverse('time_manager:category_create'), {'name': ''})

    assert response.status_code == 200
    assert 'name' in response.context['form'].errors
    assert Category.objects.filter(user=user).count() == 0


@pytest.mark.django_db
def test_category_create_rejects_duplicate_name(client, user, category):
    client.force_login(user)

    response = client.post(reverse('time_manager:category_create'), {'name': category.name})

    assert response.status_code == 200
    assert 'name' in response.context['form'].errors
    assert Category.objects.filter(user=user, name=category.name).count() == 1
