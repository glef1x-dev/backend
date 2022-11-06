from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path

api = [
    path('v1/', include('app.urls.v1', namespace='v1')),
]

urlpatterns = [
    path('api/', include(api)),
]

# Our real admin panel is written with react-admin
if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
        path('baton/', include('baton.urls')),
    ]
