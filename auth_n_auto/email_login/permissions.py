from rest_framework.permissions import BasePermission

from .models import BlackListedToken

class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        print('Is_T_V')
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
