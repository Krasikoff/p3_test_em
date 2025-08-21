# from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User

from django.core.exceptions import PermissionDenied


@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    raise PermissionDenied


User._meta.get_field("email").blank = False
