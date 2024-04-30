from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import Users, UserOperation
from utils.user_exists import UserExists


def login_form(request):
    return render(request, "login.html", {"page_title": "ログイン"})

def login_check(request):
    email = request.POST.get("email")
    password = request.POST.get("password")

    user_exists = UserExists(email, password)
    check_response = user_exists.exist_check()

    if check_response["status"]:
        user = Users.objects.filter(email=email).first()
        user_id = user.id
        user_name = user.name
        request.session["user_id"] = user_id
        user = authenticate(request, username=user_name, password=password)
        login(request, user)
        messages.success(request, 'ログインしました。')
        return redirect("/diary/")
    else:
        messages.error(request, check_response["message"])
        return redirect("login")
    

def signup(request):
    return render(request, "signup.html", {"page_title": "新規登録"})

def create_user(request):
    email = request.POST.get("email")
    name = request.POST.get("name")
    password = request.POST.get("password")

    exist_check = UserExists(email, password)
    check_response = exist_check.duplication_check()

    if not check_response["status"]:
        messages.error(request, check_response["message"])
        return redirect("signup")
    else:
        auth = 1
        password = make_password(password)
        user = Users(email=email, name=name, password=password, auth=auth)
        user.save()
        messages.success(request, "ユーザ登録が完了しました")
        return redirect("login")

def logout(request):
    request.session.flush()
    return redirect("login")



