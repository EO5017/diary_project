from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView
from .models import Users, UserOperation
from utils.user_exists import UserExists
from utils.user_crud import UserCRUD

def login_form(request):
    return render(request, "login.html", {"page_title": "ログイン"})

def login_exec(request):
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

    if check_response["status"] == False:
        messages.error(request, check_response["message"])
        return redirect("signup")
    else:
        user_crud = UserCRUD()
        result = user_crud.create_user(email, name, password)
        if result["status"] == False:
            messages.error(request, result["message"])
            return redirect("signup")
        else:
            messages.success(request, "ユーザ登録が完了しました")
            return redirect("login")

def logout(request):
    request.session.flush()
    return redirect("login")


def password_reset(request):
    return render(request, "password_reset.html", {"page_title": "パスワードリセット"})

def password_reset_exec(request):
    email = request.POST.get("email")
    user = Users.objects.filter(email=email).first()
    if user is None:
        messages.error(request, "入力されたメールアドレスは登録されていません")
        return redirect("password_reset")
    else:
        password = get_random_string(length=8)
        user_crud = UserCRUD()
        result = user_crud.update_password(email, password)
        if result['status'] == False:
            messages.error(request, result['message'])
            return redirect("password_reset")

        # send_mail('タイトル','本文','from@example.com',['to@example.com'],fail_silently=False,)
        send_mail(
            "パスワードリセット",
            f"パスワードをリセットしました。\n新しいパスワード: {password}",
            'sample000licenses@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect("password_reset_complete")


def password_reset_complete(request):
    return render(request, "password_reset_success.html", {"page_title": "パスワードリセット完了"})