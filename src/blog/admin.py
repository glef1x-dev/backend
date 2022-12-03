from django.contrib import admin

from app.admin import ModelAdmin
from blog.models import Article
from blog.models import ArticleLike
from blog.models import ArticleTag
from blog.models import ArticleTagItem


class BlogPostTagInline(admin.TabularInline):
    model = ArticleTagItem
    extra = 1


@admin.register(Article)
class ArticleAdminModel(ModelAdmin):
    inlines = (BlogPostTagInline,)


@admin.register(ArticleTag)
class ArticleTagAdminModel(ModelAdmin):
    pass


@admin.register(ArticleLike)
class ArticleLikeAdminModel(ModelAdmin):
    pass


admin.register(ArticleTagItem)
