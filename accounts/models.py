from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    pass
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=BaseUserManager.normalize_email(email))
        user.name = name
        user.set_password(password)
        user.auth = 1
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        user=self.create_user(
                name,
                email,
                password=password
            )
        user.auth = 0
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    auth = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    USERNAME_FIELD = "name"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]
    objects = UserManager()


class UserOperation(models.Model):
    user_id = models.BigIntegerField()
    ip_address = models.CharField(max_length=100)
    operation = models.CharField(max_length=100)
    event_date = models.DateTimeField(auto_now_add=True)
    memo = models.TextField()

    class Meta:
        db_table = 'user_operation'

class UserAuth(models.Model):
    auth = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_auth'
