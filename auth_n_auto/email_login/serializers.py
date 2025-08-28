from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.db import DataError

from .models import BlackListedToken, Profile
from drf_role.models import Role

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Ощуществляет сериализацию и десериализацию объектов
    User при регистрации.
    """

    password_chk = serializers.SerializerMethodField("confirm_password")

    def validate(self, attrs):
        password_chk = self.initial_data.get("password_chk", None)
        password = self.initial_data.get("password", None)
        if password and password_chk and password != password_chk:
            raise serializers.ValidationError("Passwords do not match.")
        return super().validate(attrs)

    def confirm_password(self, instance):
        return self.initial_data["password"]

    class Meta:
        fields = (
            "username",
            "email",
            "password",
            "password_chk",
            "first_name",
            "last_name",
        )
        model = User

    def to_internal_value(self, data):
        """Шифрует пароль перед сохранением в БД."""
        if data["password"] == data["password_chk"]:
            data["password_chk"] = data["password"] = make_password(
                data["password"].encode("utf-8")
            )
        else:
            data["password"] = make_password(data["password"].encode("utf-8"))
        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["password_chk"] = data["password"] = "***"
        print(instance.id)
        data["id"] = instance.id
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = all


class UserSerializer(serializers.ModelSerializer):
    """Ощуществляет сериализацию и десериализацию объектов User."""

    role = serializers.SerializerMethodField("change_role")
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password", "role", "token", "is_active")
        read_only_fields = ("token",)

    def change_role(self, instance):
        profile = Profile.objects.get(user=instance)
        print(profile.user)
        print(self.initial_data)
        try:
            role_instance = Role.objects.get(name=self.initial_data["role"])
            print(role_instance.name)
        except Exception as e:
            print(e)
            raise DataError
        profile.role = role_instance
        try:
            profile.save()
        except Exception as e:
            print(e)
        return profile.role.name

    def update(self, instance, validated_data):
        """Выполняет обновление User."""
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance

    def delete(self, instance, validated_data):
        """Удаляет пользователя."""
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
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )

        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")
        return {
            "username": user.username,
            "token": user.token,
        }


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlackListedToken
        exclude = ()
