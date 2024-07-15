from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone

from account.manager import AccountManager
from dish.models import Dish


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True, null=True)
    first_name = models.CharField(max_length=60, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    
    def __str__(self):
        return self.email
