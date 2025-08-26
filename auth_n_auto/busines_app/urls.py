from django.urls import path
from .views.mocks import ProductListView, OrderListView, StoreListView


urlpatterns = [
    path(
        "product/",
        ProductListView.as_view(),
    ),
    path("order/", OrderListView.as_view()),
    path("store/", StoreListView.as_view()),
]
