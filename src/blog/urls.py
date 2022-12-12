from rest_framework import routers

from blog.api import views

app_name = "blog"

router = routers.DefaultRouter()
router.register(r"articles", views.ArticleViewSet, basename="article")

urlpatterns = router.urls
