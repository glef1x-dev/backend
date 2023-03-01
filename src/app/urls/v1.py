from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView

from django.urls import include
from django.urls import path

app_name = "api_v1"
urlpatterns = [
    path("auth/", include("a12n.urls")),
    path("users/", include("users.urls")),
    path("blog/", include("blog.urls")),
    path("third-party/", include("third_party.urls")),
    path("healthchecks/", include("health_check.urls")),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
