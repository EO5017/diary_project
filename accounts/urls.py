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

from . import views

urlpatterns = [
    path("", views.login_form, name="login"),
    path("login_exec", views.login_exec, name="login_exec"),
    path("signup", views.signup, name="signup"),
    path("create_user", views.create_user, name="create_user"),
    path("logout", views.logout, name="logout"),
    path("password_reset", views.password_reset, name="password_reset"),
    path("password_reset_exec", views.password_reset_exec, name="password_reset_exec"),
    path("password_reset_complete", views.password_reset_complete, name="password_reset_complete"),
]
