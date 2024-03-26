from django.db import models

# Create your models here.
class Diary(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    create_user= models.CharField(max_length=100)
    update_user= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    auth = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)