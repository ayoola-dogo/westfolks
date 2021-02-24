from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("You must provide an email address")
        if not first_name:
            raise ValueError("You must provide a first name")
        if not last_name:
            raise ValueError("You must provide a last name")
        if not password:
            raise ValueError("You must have a password")
        user = self.model(
            email=self.normalize_email(email=email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email=email),
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_staff = True
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email=email),
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # email and password are required by default
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return "user-{}".format(self.email)

    def get_first_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def get_last_name(self):
        if self.last_name:
            return self.last_name
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'auth_user'
