from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Users, UserOperation
from utils.user_exists import UserExists
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def login(request):
    return render(request, "login.html", {"page_title": "ログイン"})

def login_check(request):
    mail_address = request.POST.get("mail_address")
    password = request.POST.get("password")

    user_exists = UserExists(mail_address, password)
    check_response = user_exists.exist_check()

    if check_response["status"]:
        return redirect("/diary/")
    else:
        messages.error(request, check_response["message"])
        return redirect("login")
    

def signup(request):
    return render(request, "signup.html", {"page_title": "新規登録"})

def create_user(request):
    mail_address = request.POST.get("mail_address")
    name = request.POST.get("name")
    password = request.POST.get("password")

    exist_check = UserExists(mail_address, password)
    check_response = exist_check.duplication_check()

    if not check_response["status"]:
        messages.error(request, check_response["message"])
        return redirect("signup")
    else:
        auth = 1
        password = make_password(password)
        user = Users(mail_address=mail_address, name=name, password=password, auth=auth)
        user.save()
        messages.success(request, "ユーザ登録が完了しました")
        return redirect("login")

def logout(request):
    return redirect("login")



