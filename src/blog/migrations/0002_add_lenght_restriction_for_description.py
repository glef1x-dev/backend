# Generated by Django 4.1.3 on 2022-11-03 00:23

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="description",
            field=models.CharField(
                max_length=300, verbose_name="Description of the article"
            ),
        ),
    ]
