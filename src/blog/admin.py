from django.contrib import admin

from app.admin import ModelAdmin
from blog.models import ArticleTagItem, Article, ArticleTag


class BlogPostTagInline(admin.TabularInline):
    model = ArticleTagItem
    extra = 1


@admin.register(Article)
class ArticleAdminModel(ModelAdmin):
    inlines = (BlogPostTagInline,)


@admin.register(ArticleTag)
class ArticleTagAdminModel(ModelAdmin):
    pass


admin.register(ArticleTagItem)
