from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

api = [
    path("v1/", include("app.urls.v1", namespace="v1")),
]

urlpatterns = [
    path("api/", include(api)),
    path("", include("django_prometheus.urls")),
]

# Our real admin panel is written with react-admin
if settings.DEBUG:
    urlpatterns += [
        path("admin/", admin.site.urls),
        path("baton/", include("baton.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
