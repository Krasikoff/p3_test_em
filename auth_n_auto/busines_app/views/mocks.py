from drf_mocker.viewsets import MockViewSet
from drf_mocker.views import MockListAPIView
from rest_framework import serializers


class ProductListMock(MockViewSet):
    def get_permissions(self):
        print('permission_classes =', self.permission_classes)
        return super().get_permissions()

    json_filename = "product_list.json"
    mock_status = 200
    delay_seconds = 1


class StubSerializer(serializers.BaseSerializer):
    """stub сериалайзер"""
    pass


class OrderListView(MockListAPIView):
    def get_serializer_class(self):
        return StubSerializer

    json_filename = "order_list.json"
    mock_status = 200
    delay_seconds = 1
