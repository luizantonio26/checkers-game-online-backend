
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views.user_view import UserViewSet
from authentication.views.verify_account_view import VerifyAccountView


# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/register/', UserViewSet.as_view({"post": "register"}), name="user_register"),
    path('auth/login/', UserViewSet.as_view({"post": "login"}), name="user_login"),
    path('auth/test/', UserViewSet.as_view({"get": "authenticated_route_test"}), name="authenticated_route_test"),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('auth/otp/', VerifyAccountView.as_view({"post": "send_otp_code"}), name="send_otp_code"),
    path('auth/otp/verify/<str:otp>/', VerifyAccountView.as_view({"get": "verify_otp"}), name="verify_otp"),
]
