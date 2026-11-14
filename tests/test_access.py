import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_access_only_for_logged_users(client):
    response = client.get(reverse("dashboard:dashboard"))

    assert response.status_code == 302
    assert response.url.startswith("/login/")


def test_login_access_for__not_logged_users(client):
    response = client.get(reverse("login"))

    assert response.status_code == 200
