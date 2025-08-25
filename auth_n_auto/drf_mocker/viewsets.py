from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_role.permissions import IsAdminOrNoAccess, BaseRolePermission

from .mixins import FileMockResponseMixin


class MockViewSet(FileMockResponseMixin, ViewSet):
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [BaseRolePermission]
            print(self.action, permission_classes)
        else:
            permission_classes = [IsAdminOrNoAccess]
        return [permission() for permission in permission_classes]    
    
    def list(self, request):
        return Response(self.get_mock_data(), status=self.mock_status)

    def retrieve(self, request, pk=None):
        return Response(self.get_mock_data(), status=self.mock_status)

    def create(self, request):
        return Response(self.get_mock_data(), status=self.mock_status)

    def update(self, request, pk=None):
        return Response(self.get_mock_data(), status=self.mock_status)

    def destroy(self, request, pk=None):
        return Response(self.get_mock_data(), status=self.mock_status)
