from django.urls import path, include

from blog.api import viewsets

app_name = 'blog'
urlpatterns = [
    path('articles/', include(
        [
            path('', viewsets.CreateListArticlesAPIViewSet.as_view(
                {
                    'get': 'list',
                    'post': 'create'
                }
            ), name='retrieve-or-create-articles'),
            path('<slug:slug>/', viewsets.DeleteRetrieveUpdateArticleViewSet.as_view(
                {
                    'get': 'retrieve',
                    'delete': 'destroy',
                    'patch': 'update'
                }
            ), name='retrieve-article-by-slug'),
        ]
    ))
]
