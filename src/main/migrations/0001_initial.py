# Generated by Django 4.1.13 on 2024-07-05 14:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('author', models.CharField(max_length=255, verbose_name='Author')),
                ('published_date', models.DateField(verbose_name='Published date')),
                ('genre', models.CharField(max_length=100, verbose_name='Genre')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Price')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
                'ordering': ['-created'],
            },
        ),
    ]
