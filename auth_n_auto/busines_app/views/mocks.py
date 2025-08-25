from drf_mocker.viewsets import MockViewSet
from drf_role.permissions import IsAdminOrNoAccess, BaseRolePermission
from rest_framework.permissions import AllowAny, IsAuthenticated

class ProductListMock(MockViewSet):
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [BaseRolePermission]
            print(permission_classes)
        else:
            permission_classes = [IsAdminOrNoAccess]

        return [permission() for permission in permission_classes]
    json_filename = "product_list.json"
    mock_status = 200
    delay_seconds = 1
