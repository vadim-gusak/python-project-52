from django.test import TestCase
from django.contrib.auth.models import User
from .models import Status
from django.urls import reverse
from urllib.parse import urlencode


class TestStatusesView(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create(
            first_name="Bob",
            last_name="WoW",
            username="wiku",
        )
        user1.set_password("Pukote74.")
        user1.save()

        self.statuses = [
            Status.objects.create(name="Ready!!!"),
            Status.objects.create(name="In progress"),
            Status.objects.create(name="Error"),
        ]
        for status in self.statuses:
            status.save()

        return super().setUp()

    def test_view_get_all_statuses(self):
        self.client.login(username="wiku", password="Pukote74.")
        resp = self.client.get(reverse("statuses"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "status/statuses.html")
        self.assertListEqual(list(resp.context["statuses"]), self.statuses)


class TestStatusCreate(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create(
            first_name="Bob",
            last_name="WoW",
            username="wiku",
        )
        user1.set_password("Pukote74.")
        user1.save()
        return super().setUp()

    def test_view_get(self):
        self.client.login(username="wiku", password="Pukote74.")
        resp = self.client.get(reverse("create_status"))

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "status/create.html")

        self.client.logout()
        resp = self.client.get(reverse("create_status"), follow=True)
        message = list(resp.context.get("messages"))[0]

        self.assertRedirects(resp, reverse("login"))
        self.assertEqual(message.tags, "error")

    def test_view_post(self):
        self.client.login(username="wiku", password="Pukote74.")
        resp = self.client.post(
            reverse("create_status"),
            urlencode({"name": "Fogotten"}),
            content_type="application/x-www-form-urlencoded",
            follow=True,
        )
        message = list(resp.context.get("messages"))[0]

        self.assertRedirects(resp, reverse("statuses"))
        self.assertEqual(message.tags, "success")

        self.client.logout()
        resp = self.client.post(
            reverse("create_status"),
            urlencode({"value": "Fogotten"}),
            content_type="application/x-www-form-urlencoded",
            follow=True,
        )
        message = list(resp.context.get("messages"))[0]

        self.assertRedirects(resp, reverse("login"))
        self.assertEqual(message.tags, "error")


class TestStatusUpdate(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create(
            first_name="Bob",
            last_name="WoW",
            username="wiku",
        )
        user1.set_password("Pukote74.")
        user1.save()

        self.statuses = [
            Status.objects.create(name="Ready!!!"),
            Status.objects.create(name="In progress"),
            Status.objects.create(name="Error"),
        ]
        for status in self.statuses:
            status.save()

        return super().setUp()

    def test_view_get(self):
        self.client.login(username="wiku", password="Pukote74.")
        resp = self.client.get("/statuses/3/update/")

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "status/update.html")

        self.client.logout()
        resp = self.client.get("/statuses/3/update/", follow=True)
        message = list(resp.context.get("messages"))[0]

        self.assertRedirects(resp, reverse("login"))
        self.assertEqual(message.tags, "error")

    def test_view_post(self):
        self.client.login(username="wiku", password="Pukote74.")
        resp = self.client.post(
            reverse("update_status", kwargs={"pk": 1}),
            urlencode({"name": "Fogotten"}),
            content_type="application/x-www-form-urlencoded",
            follow=True,
        )
        message = list(resp.context.get("messages"))[0]

        self.assertRedirects(resp, reverse("statuses"))
        self.assertEqual(message.tags, "success")

        self.client.logout()
        resp = self.client.post(
            reverse("update_status", kwargs={"pk": 2}),
            urlencode({"value": "Fogotten"}),
            content_type="application/x-www-form-urlencoded",
            follow=True,
        )
        message = list(resp.context.get("messages"))[0]

        self.assertRedirects(resp, reverse("login"))
        self.assertEqual(message.tags, "error")


class TestStatusDelete(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create(
            first_name="Bob",
            last_name="WoW",
            username="wiku",
        )
        user1.set_password("Pukote74.")
        user1.save()

        self.statuses = [
            Status.objects.create(name="Ready!!!"),
            Status.objects.create(name="In progress"),
            Status.objects.create(name="Error"),
        ]
        for status in self.statuses:
            status.save()

        return super().setUp()

    def test_view_get(self):
        self.client.login(username="wiku", password="Pukote74.")
        resp = self.client.get("/statuses/3/delete/")

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "status/delete.html")

        self.client.logout()
        resp = self.client.get("/statuses/3/delete/", follow=True)
        message = list(resp.context.get("messages"))[0]

        self.assertRedirects(resp, reverse("login"))
        self.assertEqual(message.tags, "error")

    def test_view_post(self):
        """

        ДОБАВИТЬ ПРОВЕРКУ ИСПОЛЬЗОВАНИЯ В ЗАДАЧАХ!!!

        """

        self.client.login(username="wiku", password="Pukote74.")
        resp = self.client.post(
            reverse("delete_status", kwargs={"pk": 1}),
            content_type="application/x-www-form-urlencoded",
            follow=True,
        )
        message = list(resp.context.get("messages"))[0]

        self.assertRedirects(resp, reverse("statuses"))
        self.assertEqual(message.tags, "success")

        self.client.logout()
        resp = self.client.post(
            reverse("update_status", kwargs={"pk": 2}),
            content_type="application/x-www-form-urlencoded",
            follow=True,
        )
        message = list(resp.context.get("messages"))[0]

        self.assertRedirects(resp, reverse("login"))
        self.assertEqual(message.tags, "error")
