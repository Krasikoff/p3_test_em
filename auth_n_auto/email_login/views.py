from email_login.serializers import (
    RegistrationSerializer,
    UserSerializer,
    LoginSerializer,
    LogoutSerializer,
)
from django.db import DatabaseError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, mixins, views, generics
from django.contrib.auth import get_user_model
from rest_framework import status, response
from .models import BlackListedToken, Profile
from drf_role.models import Role
from drf_role.enums import RoleEnum

User = get_user_model()


class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Register for anonymous.
    """

    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):        
        serializer.save()
        user_for_profile = User.objects.get(id=serializer.data['id'])
        role = Role.objects.get(name=RoleEnum.Buyer.name)
        Profile.objects.get_or_create(user=user_for_profile, role=role)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    update, delete current user.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        request.data["is_active"] = "false"
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(views.APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            BlackListedToken.objects.filter(user__username=serializer.data['username']).prefetch_related().delete()
        except DatabaseError as e:
            print(e)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(views.APIView):
    """
    Logs out an existing user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        """Помещает в блэклист."""
        serializer = self.serializer_class(data={"token": request.auth, "user": request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            {"message": "Logged out successfully"}, status=200
        )
