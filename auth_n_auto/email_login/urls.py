from django.urls import include, path
from rest_framework.routers import DefaultRouter

from email_login.views import (
    RegistrationViewSet,
    UpdateUserViewSet,
    DestroyUserViewSet,
    LoginAPIView,
)


router_v1 = DefaultRouter()
router_v1.register('registration', RegistrationViewSet, basename='registration')
router_v1.register('update_user', UpdateUserViewSet, basename='update_user')
router_v1.register('delete_user', DestroyUserViewSet, basename='delete_user')


urlpatterns = [
    path('v1/', include(router_v1.urls), name='api-root'),
    path('v1/login', LoginAPIView.as_view(), name='login')
]