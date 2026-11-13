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