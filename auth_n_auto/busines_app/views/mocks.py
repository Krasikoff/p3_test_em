from django.http import JsonResponse
from rest_framework import serializers, generics


class StubSerializer(serializers.BaseSerializer):
    """stub сериалайзер"""

    pass


class ProductListView(generics.ListAPIView):
    def get_permissions(self):
        print("permission_classes =", self.permission_classes)
        return super().get_permissions()

    def get_serializer_class(self):
        return StubSerializer

    def list(self, *args, **kwargs):
        return JsonResponse(data={"data": "Product_data"})


class OrderListView(generics.ListAPIView):
    def get_permissions(self):
        print("permission_classes =", self.permission_classes)
        return super().get_permissions()

    def get_serializer_class(self):
        return StubSerializer

    def list(self, *args, **kwargs):
        return JsonResponse(data={"data": "Order_data"})


class StoreListView(generics.ListAPIView):
    def get_permissions(self):
        print("permission_classes =", self.permission_classes)
        return super().get_permissions()

    def get_serializer_class(self):
        return StubSerializer

    def list(self, *args, **kwargs):
        return JsonResponse(data={"data": "Store_data"})
