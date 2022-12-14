# Generated by Django 4.1.3 on 2022-12-03 20:54

from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_add_article_likes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articlelike",
            name="article",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="blog.article",
            ),
        ),
        migrations.AlterField(
            model_name="articlelike",
            name="ip_address",
            field=models.GenericIPAddressField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name="articlelike",
            unique_together={("browser_fingerprint", "article")},
        ),
    ]
