from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    mail_address = models.CharField(max_length=200, unique=True)
    auth = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'


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
