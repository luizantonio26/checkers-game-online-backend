
from django.urls import include, path
from rest_framework import routers

from authentication.views.user_view import UserViewSet


# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/register/', UserViewSet.as_view({"post": "register"}), name="user_register"),
    path('auth/login/', UserViewSet.as_view({"post": "login"}), name="user_login"),
    path('auth/test/', UserViewSet.as_view({"get": "authenticated_route_test"}), name="authenticated_route_test"),
]
