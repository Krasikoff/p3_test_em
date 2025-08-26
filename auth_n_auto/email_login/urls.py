from django.urls import include, path
from rest_framework.routers import DefaultRouter

from email_login.views import (
    RegistrationViewSet,
    LoginAPIView,
    LogoutAPIView,
    UserRetrieveUpdateAPIView,
#    JWTAccessToken,
)


router_v1 = DefaultRouter()
router_v1.register('registration', RegistrationViewSet, basename='registration')

urlpatterns = [
    path('v1/', include(router_v1.urls), name='api-root'),
    path('v1/login/', LoginAPIView.as_view(), name='login'),
    path('v1/logout/', LogoutAPIView.as_view(), name='logout'),
    path('v1/user/', UserRetrieveUpdateAPIView.as_view()),
]