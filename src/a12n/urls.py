from django.urls import path

from a12n.api import views

app_name = 'a12n'
urlpatterns = [
    path('token/', views.ObtainJSONWebTokenView.as_view(), name='obtain-token'),
    path('token/refresh/', views.RefreshJSONWebTokenView.as_view(), name='refresh-token'),
    path('token/verify/', views.VerifyJSONWebTokenView.as_view(), name='verify-token'),
    path('token/blacklist/', views.BlacklistJSONWebTokenView.as_view(), name='blacklist-token'),
]
