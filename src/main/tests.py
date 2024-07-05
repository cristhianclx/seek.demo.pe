# -*- coding:UTF-8 -*-

import random
from unittest.mock import patch

from django.urls import reverse

from bson.decimal128 import Decimal128
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase as TestCase

from accounts.models import User

from .constants import BOOK_GENRE_CHOICES, BOOK_GENRE_FICTION, BOOK_GENRE_NON_FICTION
from .models import Book

fake = Faker()


class BookViewSetTest(TestCase):
    def setUp(self):
        self.user_name = fake.name()
        self.user_email = fake.email()
        self.user_password = fake.password()
        self.user = User.objects.create_user(name=self.user_name, email=self.user_email, password=self.user_password)
        self.client.force_authenticate(user=self.user)
        Book.objects.create(
            title=" ".join(fake.words(nb=random.randint(2, 4))).title(),
            author=fake.name(),
            genre=BOOK_GENRE_FICTION,
            published_date=fake.past_date(),
            price=fake.random_number(digits=2),
        )
        Book.objects.create(
            title=" ".join(fake.words(nb=random.randint(2, 4))).title(),
            author=fake.name(),
            genre=BOOK_GENRE_NON_FICTION,
            published_date=fake.past_date(),
            price=fake.random_number(digits=2),
        )

    @patch("pymongo.collection.Collection.aggregate")
    def test_average_price(self, mock_aggregate):
        mock_aggregate.return_value = [{"_id": None, "price_average": Decimal128("25.00")}]
        url = reverse("books-average-price", kwargs={"year": "2021"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"year": "2021", "price": {"average": 25.00}})

    @patch("pymongo.collection.Collection.aggregate")
    def test_average_price_no_data(self, mock_aggregate):
        mock_aggregate.return_value = []
        url = reverse("books-average-price", kwargs={"year": "2021"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"year": "2021", "price": {"average": "No data available for this year."}})

    def test_genres(self):
        url = reverse("books-genres")
        response = self.client.get(url)
        expected_data = [{"id": genre_choice[0], "name": genre_choice[1]} for genre_choice in BOOK_GENRE_CHOICES]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, expected_data)

    def test_list_books(self):
        url = reverse("books-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        book = Book.objects.first()
        url = reverse("books-detail", kwargs={"id": book.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], book.title)
