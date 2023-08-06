from django.db import models
from django.conf import settings 
from django.contrib.auth import get_user_model 
from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager
)
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Person(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField('First Name', max_length=25)
    last_name = models.CharField('Last Name', blank=True, max_length=25)
    email = models.EmailField('Email', unique=True,
                              db_index=True)
    is_staff = models.BooleanField('Is staff user', default=False)
    is_app_user = models.BooleanField('Is Application user', default=False)
    is_active = models.BooleanField('Active', default=False)
    date_joined = models.DateField('Joined Date', blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return '{0}'.format(self.first_name)

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name







