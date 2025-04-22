from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, role, username, password=None, **extra_fields):
        if not role:
            raise ValueError("The Role field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        user = self.model(role=role, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, role, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(role=role, username=username, password=password, **extra_fields)


class User(AbstractBaseUser):
    role = models.CharField(max_length=15)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["role"]

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, bidding):
        return self.is_superuser

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["id"]