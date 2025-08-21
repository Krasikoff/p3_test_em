#from django.shortcuts import render
from email_login.serializers import UserSerializer, UpdateUserSerializer, LoginSerializer
from rest_framework import viewsets, mixins, views
from django.contrib.auth import get_user_model
from rest_framework import status, response

User = get_user_model()

class RegistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def perform_create(self, serializer):
        serializer.save()
class UpdateUserViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = isinstance
    serializer_class = UpdateUserSerializer

class DestroyUserViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = isinstance
    serializer_class = UpdateUserSerializer

class LoginAPIView(views.APIView):
    """
    Logs in an existing user.
    """
    # permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return response.Response(serializer.data, status=status.HTTP_200_OK)
