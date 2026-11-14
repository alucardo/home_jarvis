import pytest
from django.urls import reverse

from time_manager.models import Category, TimeEntry
from time_manager.tests.factories import CategoryFactory, TimeEntryFactory

pytestmark = pytest.mark.django_db


def test_category_index_shows_only_own_categories(client, user, other_user, category):
    CategoryFactory(name="secret", user=other_user)
    client.force_login(user)

    response = client.get(reverse("time_manager:category_index"))

    html = response.content.decode()
    assert response.status_code == 200
    assert category.name in html
    assert "secret" not in html


def test_create_category_get_view_success(client, user):
    client.force_login(user)
    response = client.get(reverse("time_manager:category_create"))

    assert response.status_code == 200


def test_category_create(client, user):
    client.force_login(user)
    response = client.post(reverse("time_manager:category_create"), {"name": "secret"})

    assert response.status_code == 302
    assert response.url == reverse("time_manager:category_index")
    assert Category.objects.filter(user=user, name="secret").exists()


def test_category_create_reject_empty_name(client, user):
    client.force_login(user)
    response = client.post(reverse("time_manager:category_create"), {"name": ""})

    assert response.status_code == 200
    assert "name" in response.context["form"].errors
    assert Category.objects.filter(user=user).count() == 0


def test_category_create_rejects_duplicate_name(client, user, category):
    client.force_login(user)

    response = client.post(reverse("time_manager:category_create"), {"name": category.name})

    assert response.status_code == 200
    assert "name" in response.context["form"].errors
    assert Category.objects.filter(user=user, name=category.name).count() == 1


def test_category_edit_get_shows_form_with_current_name(client, user, category):
    client.force_login(user)

    response = client.get(reverse("time_manager:category_edit", kwargs={"pk": category.id}))

    assert response.status_code == 200
    form = response.context["form"]
    assert form.initial["name"] == category.name


def test_category_edit_post_updates_name_and_redirect(client, user, category):
    client.force_login(user)
    new_name = "new name"

    response = client.post(reverse("time_manager:category_edit", kwargs={"pk": category.id}), {"name": new_name})

    assert response.status_code == 302
    assert response.url == reverse("time_manager:category_index")
    category.refresh_from_db()
    assert category.name == new_name


def test_category_edit_post_updates_with_the_same_name(client, user, category):
    client.force_login(user)

    response = client.post(reverse("time_manager:category_edit", kwargs={"pk": category.id}), {"name": category.name})

    assert response.status_code == 302
    assert response.url == reverse("time_manager:category_index")


def test_category_edit_rejects_name_of_another_own_category(client, user, category):
    second_category = CategoryFactory(user=user)
    client.force_login(user)

    response = client.post(
        reverse("time_manager:category_edit", kwargs={"pk": category.id}), {"name": second_category.name}
    )

    assert response.status_code == 200
    form = response.context["form"]
    assert "name" in form.errors
    assert "Taka kategoria już istnieje." in form.errors["name"]


def test_category_edit_allow_the_same_name_with_other_user(client, user, category):
    second_category = CategoryFactory()
    client.force_login(user)

    response = client.post(
        reverse("time_manager:category_edit", kwargs={"pk": category.id}), {"name": second_category.name}
    )

    assert response.status_code == 302
    assert response.url == reverse("time_manager:category_index")
    category.refresh_from_db()
    assert category.name == second_category.name


def test_category_edit_other_user_category_not_found(client, other_user, category):
    client.force_login(other_user)

    response = client.post(reverse("time_manager:category_edit", kwargs={"pk": category.id}), {"name": "new name"})

    assert response.status_code == 404


def test_category_delete_when_correct_removes_and_redirect_user(client, user, category):
    client.force_login(user)

    response = client.post(reverse("time_manager:category_delete", kwargs={"pk": category.id}))

    assert response.status_code == 302
    assert response.url == reverse("time_manager:category_index")
    assert not Category.objects.filter(id=category.id).exists()


def test_category_delete_when_removing_removes_time_entry(client, user, category):
    client.force_login(user)
    time_entry = TimeEntryFactory(user=user, category=category)
    time_entry_form_other_category = TimeEntryFactory(user=user)

    client.post(reverse("time_manager:category_delete", kwargs={"pk": category.id}))

    assert not TimeEntry.objects.filter(id=time_entry.id).exists()
    assert TimeEntry.objects.filter(id=time_entry_form_other_category.id).exists()


def test_category_delete_when_removing_not_existing_returns_404(client, user, category):
    category_id = category.id
    category.delete()
    client.force_login(user)

    response = client.post(reverse("time_manager:category_delete", kwargs={"pk": category_id}))

    assert response.status_code == 404


def test_category_delete_when_removing_not_users_returns_404(client, other_user, category):
    client.force_login(other_user)

    response = client.post(reverse("time_manager:category_delete", kwargs={"pk": category.id}))

    assert response.status_code == 404
    assert Category.objects.filter(id=category.id).exists()


def test_category_delete_when_get_request_gets_405(client, user, category):
    client.force_login(user)

    response = client.get(reverse("time_manager:category_delete", kwargs={"pk": category.id}))

    assert response.status_code == 405
    assert Category.objects.filter(id=category.id).exists()
