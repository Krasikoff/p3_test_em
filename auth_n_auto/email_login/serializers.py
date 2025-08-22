from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов User при регистрации. """
    class Meta:
        fields = ( 'username', 'email', 'password', 'first_name', 'last_name',)
        model = User

    def to_internal_value(self, data):
        """ Шифрует пароль перед сохранением в БД. """
        hashed = make_password(data['password'].encode('utf-8'))
        print(hashed)
        data['password'] = hashed
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    """ Ощуществляет сериализацию и десериализацию объектов User. """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token','is_active')
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """ Выполняет обновление User. """
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def delete(self, instance, validated_data):
        """ Удаляет пользователя. """
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    """
    Аутенфикация существующего пользователя.
    Требуются email и password.
    Возвращает a JSON web token.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Валидация user data.
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
            'email': user.email,
            'username': user.username,
            'token': user.token,
        }
