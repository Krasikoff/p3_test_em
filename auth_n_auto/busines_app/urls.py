from django.urls import path, include
from .views.mocks import ProductListMock, OrderListView
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('products', ProductListMock, basename='products')

urlpatterns = [
    path('', include(router_v1.urls), name='busines'),
    path("order/", OrderListView.as_view()),
]
