from django.urls import resolve
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.exceptions import NotAuthenticated

from drf_role.enums import RoleEnum, PermissionEnum
from drf_role.models import AccessControl
from email_login.models import BlackListedToken


class IsAdminOrNoAccess(permissions.IsAuthenticated):

    @staticmethod
    def is_token_valid(request=None, view=None):
        user_id = request.user.id
        is_allowed_user = True
        token = request.auth
        try:
            is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
            if is_blackListed:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user

    def has_permission(self, request, view):
        if not self.is_token_valid(request=request):
            raise NotAuthenticated
        try:
            return request.user.profile.role.type == RoleEnum.Admin.value
        except AttributeError:
            return False


class BaseRolePermission(BasePermission):
    SAFE_MODELS = list()

    @staticmethod
    def permission_analyzer(request=None, view=None):
        """
        Analyze the permissions and model object level permission
        """
        try:
            user = request.user
            print('user =', user)
            user_role = user.profile.role
            print('user_role =', user_role)
            url_name = resolve(request.path_info).url_name
            access = AccessControl.objects.filter(
                role_id=user_role.pk, url_name=url_name
            ).first()
            print('url_name =', url_name)
            if access:
                permission_types = access.permissions.values_list(
                    "access_type", flat=True
                )
                write_permission = PermissionEnum.WRITE.value
                no_access = PermissionEnum.NO_ACCESS.value

                if no_access in permission_types:
                    print('permission = NO_ACCESS')
                    return False
                if write_permission in permission_types:
                    print('permission = WRITE')
                    return True
                else:
                    print('permission = READ')
                    return request.method in SAFE_METHODS
            else:
                return True
        except AttributeError:
            return False
        
    @staticmethod
    def is_token_valid(request=None, view=None):
        user_id = request.user.id
        is_allowed_user = True
        token = request.auth
        try:
            print(user_id, token)
            is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
            if is_blackListed:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        print(is_allowed_user)
        return is_allowed_user


    def has_permission(self, request, view):
        if not self.is_token_valid(request=request):
            raise NotAuthenticated
        return self.permission_analyzer(request=request)

    def has_object_permission(self, request, view, obj):
        if not self.is_token_valid(request=request):
            return False
        return self.permission_analyzer(request=request)
