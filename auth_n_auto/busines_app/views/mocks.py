from drf_mocker.viewsets import MockViewSet


class ProductListMock(MockViewSet):
    def get_permissions(self):
        print('permission_classes =', self.permission_classes)
        return super().get_permissions()

    json_filename = "product_list.json"
    mock_status = 200
    delay_seconds = 1
