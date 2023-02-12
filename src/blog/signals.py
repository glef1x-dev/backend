from django.core.cache import cache
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import Article


@receiver(post_delete, sender=Article)
@receiver(post_save, sender=Article)
def object_post_delete_handler(*args, **kwargs):
    cache.delete("articles")
