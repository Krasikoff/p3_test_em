from django.urls import re_path

from drf_role.views import (
    RoleView,
    PermissionView,
    AccessControlView,
    AllUrlList
)

urlpatterns = [
    re_path(r"^roles/", RoleView.as_view()),
    re_path(r"^permissions/", PermissionView.as_view()),
    re_path(r"^accesses/", AccessControlView.as_view()),
    re_path(r"^all-urls/", AllUrlList.as_view()),
]
