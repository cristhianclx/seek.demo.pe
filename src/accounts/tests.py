# -*- coding:UTF-8 -*-

import base64

from django.urls import reverse

from faker import Faker
from rest_framework.test import APITestCase as TestCase

from .models import User

fake = Faker()


def get_basic_auth_header(username, password):
    return "Basic %s" % base64.b64encode((f"{username}:{password}").encode("ascii")).decode()


class UserTests(TestCase):
    def setUp(self):
        self.user_name = fake.name()
        self.user_email = fake.email()
        self.user_password = fake.password()
        self.user = User.objects.create_user(name=self.user_name, email=self.user_email, password=self.user_password)

    def test_user_registration(self):
        url = reverse("accounts-users-create")
        random_password = fake.password()
        data = {
            "name": fake.name(),
            "email": fake.email(),
            "password": random_password,
            "password_confirm": random_password,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(email=data["email"]).all().count(), 1)

    def test_login(self):
        url = reverse("knox_login")
        self.client.credentials(HTTP_AUTHORIZATION=get_basic_auth_header(self.user_email, self.user_password))
        response = self.client.post(url, json={})
        raw = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("expiry", raw)
        self.assertIn("token", raw)
        self.assertEqual(raw["user"], {"email": self.user_email, "name": self.user_name})

    def test_user_profile_update(self):
        self.client.login(email=self.user_email, password=self.user_password)
        url = reverse("accounts-users-create")
        data = {
            "email": fake.email(),
            "name": fake.name(),
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, data["name"])

    def test_password_change_success(self):
        self.client.login(email=self.user_email, password=self.user_password)
        url = reverse("accounts-user_password_change")
        new_password = fake.password()
        data = {
            "old_password": self.user_password,
            "new_password": new_password,
            "confirm_password": new_password,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 204)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    def test_password_change_failure(self):
        self.client.login(email=self.user_email, password=self.user_password)
        url = reverse("accounts-user_password_change")
        new_password = fake.password()
        data = {
            "old_password": "wrongpassword",
            "new_password": new_password,
            "confirm_password": new_password,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("old_password", response.json())
        self.assertEqual(response.json()["old_password"], "Wrong password.")
