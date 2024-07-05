# -*- coding: utf-8 -*-

from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase as TestCase

from accounts.models import User

fake = Faker()


class MeTests(TestCase):
    def setUp(self):
        self.user_name = fake.name()
        self.user_email = fake.email()
        self.user_password = fake.password()
        self.user = User.objects.create_user(name=self.user_name, email=self.user_email, password=self.user_password)
        self.client.force_authenticate(user=self.user)

    def test_data(self):
        url = reverse("me-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_email)
