from django.urls import path, include
from rest_framework.authtoken import views
from .views import home


urlpatterns = [
    path('', home, name = 'api.home'),
    # path('ascii-art/', include('api.ascii_art.urls')), remove comment after adding url in ascii_art/urls.py
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
]