from email_login.serializers import (
    RegistrationSerializer,
    UserSerializer,
    LoginSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, mixins, views, generics
from django.contrib.auth import get_user_model
from rest_framework import status, response


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

        return response.Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(views.APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        """Помещает в блэклист."""
        token_key = request.auth
        print(token_key)
        # TODO Помещает в блэклист
        return response.Response(
            {"message": "Logged out successfully"}, status=200
        )
