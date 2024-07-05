import random

from django.db import migrations

from faker import Faker

from main.constants import BOOK_GENRE_CHOICES

faker = Faker()


def add_book_data(apps, schema_editor):
    Book = apps.get_model("main", "Book")

    genres = [genre_choice[0] for genre_choice in BOOK_GENRE_CHOICES]
    books = [
        Book(
            title=' '.join(faker.words(nb=random.randint(2, 4))).title(),
            author=faker.name(),
            published_date=faker.date_between(start_date="-10y", end_date="today"),
            genre=random.choice(genres),
            price=round(random.uniform(10.0, 50.0), 1),
        )
        for _ in range(100)
    ]
    Book.objects.bulk_create(books)


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_alter_book_genre"),
    ]

    operations = [
        migrations.RunPython(add_book_data),
    ]
