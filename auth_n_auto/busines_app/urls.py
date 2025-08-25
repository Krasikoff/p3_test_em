from django.urls import path, include
from .views.mocks import ProductListMock
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('products', ProductListMock, basename='products')

urlpatterns = [
    path('', include(router_v1.urls), name='busines'),
]
# urlpatterns = [
#     path("mock/products/", ProductListMock, basename='products'),
# ]
