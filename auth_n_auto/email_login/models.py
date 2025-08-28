import jwt
from datetime import datetime, timedelta

from django.db import models

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from drf_role.models import Role

# @receiver(pre_delete, sender=User)
# def delete_user(sender, instance, **kwargs):
#     raise PermissionDenied


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        first_name,
        last_name,
        password=None,
        commit=True,
    ):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(
            self, email, username, first_name, last_name, password
    ):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        db_index=True, max_length=255, unique=True, blank=False
    )
    email = models.EmailField(
        "email address", max_length=128, unique=True, blank=False
    )
    first_name = models.CharField("first name", max_length=255, blank=True)
    last_name = models.CharField("last name", max_length=255, blank=True)

    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return "{} <{}>".format(self.username, self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.username

    def get_short_name(self):
        """Аналогично методу get_full_name()."""
        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=7)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(
        User, related_name="token_user", on_delete=models.CASCADE, unique=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")
