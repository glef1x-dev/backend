# Generated by Django 4.1.3 on 2022-11-03 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_add_lenght_restriction_for_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="image_label",
        ),
    ]
