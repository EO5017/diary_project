from django.contrib import admin

# Register your models here.
from .models import Diary, User

admin.site.register(Diary)
admin.site.register(User)
