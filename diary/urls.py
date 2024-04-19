"""
URL configuration for diary_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import index, add

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("post", views.post, name="post"),
    path("read/<int:diary_id>", views.read, name="read"),
    path("edit/<int:diary_id>", views.edit, name="edit"),
    path("delete/<int:diary_id>", views.delete, name="delete"),

    # 基本使わない
    path("add/", add.as_view(), name="add"),
]
