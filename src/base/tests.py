# -*- coding:UTF-8 -*-

from django.test import TestCase


class BaseViews(TestCase):
    def test_ping(self):
        response = self.client.get("/ping/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["response"], "pong")
        self.assertEqual(response.json()["stage"], "docker")
