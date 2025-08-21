from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ( 'username', 'email', 'password', 'first_name', 'last_name',)
        model = User

    def to_internal_value(self, data):
        hashed = make_password(data['password'].encode('utf-8'))
        print(hashed)
        data['password'] = hashed
        return super().to_internal_value(data)

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        )
        model = User


class DestroyUserSerializer(UserSerializer):
    pass        

class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
        }