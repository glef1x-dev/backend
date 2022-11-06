import factory
import pytest_factoryboy

from blog.models import ArticleTag, Article


class ArticleTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticleTag

    title = factory.Sequence(lambda n: 'Tag #%s' % n)


@pytest_factoryboy.register(name='article')
class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article
        exclude = ('image', 'image_label')

    title = 'test'
    description = 'test'
    body = 'test'

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for tag in extracted:
                self.tags.add(tag)
