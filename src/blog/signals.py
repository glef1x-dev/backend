from django.core.cache import cache
from django.db.models import QuerySet
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import Article
from blog.models import ArticleTag
from blog.utils.cache import get_all_possible_cache_keys_to_invalidate


@receiver(post_delete, sender=Article)
@receiver(post_save, sender=Article)
def object_post_delete_handler(sender, instance: Article, *args, **kwargs):
    article_tags: QuerySet[ArticleTag] = instance.tags.all()
    cache.delete_many(
        [
            *get_all_possible_cache_keys_to_invalidate(
                slug=instance.slug, tags=list(article_tags)
            )
        ]
    )
