from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Diary
from utils import datetime_utils

# Create your views here.
def index(request):
    page_title = "Diary"
    # データベースから全ての日記を取得
    diary_list = Diary.objects.all()

    # date関連をyyyy-mm-dd形式に変換
    for diary in diary_list:
        wirite_date_dtu = datetime_utils.DatetimeUtils(diary.write_date)
        diary.write_date = wirite_date_dtu.convert_into_yyyy_mm_dd()

    # render関数でテンプレートにデータを渡す
    return render(request, "index.html", {"diary_list": diary_list, "page_title": page_title})

# 鑑賞ページ
def read(request, diary_id):
    if not diary_id:
        return render(request, "error.html")
    
    page_title = "Read Diary"
    
    diary = Diary.objects.filter(id=diary_id).first()

    # date関連をyyyy-mm-dd形式に変換
    wirite_date_dtu = datetime_utils.DatetimeUtils(diary.write_date)
    diary.write_date = wirite_date_dtu.convert_into_yyyy_mm_dd()
    create_date_dtu = datetime_utils.DatetimeUtils(diary.created_at)
    diary.created_at = create_date_dtu.convert_into_yyyy_mm_dd()
    update_date_dtu = datetime_utils.DatetimeUtils(diary.updated_at)
    diary.updated_at = update_date_dtu.convert_into_yyyy_mm_dd()

    if not diary:
        return render(request, "error.html")
    
    return render(request, "read.html", {"diary": diary, "page_title": page_title})

def create(request):
    page_title = "Create Diary"

    return render(request, "edit.html", {"page_title": page_title})

def edit(request, diary_id):
    page_title = "Edit Diary"

    if not diary_id:
        return render(request, "error.html")
    
    user = 1
    diary = Diary.objects.filter(id=diary_id , user_id=user).first()

    if not diary:
        return render(request, "error.html")

    return render(request, "edit.html", {"diary": diary, "page_title": page_title})


def delete(request, diary_id):
    if not diary_id:
        return render(request, "error.html")
    
    user = 1

    diary = Diary.objects.filter(id=diary_id , user_id=user).first()
    if not diary:
        return render(request, "error.html")
    
    diary.delete()

    # indexに遷移
    return redirect("index")


def post(request):
    if not request.POST.get("diary_id"):
        # 新規登録
        diary = Diary()
    else:
        # 更新
        diary_id = request.POST.get("diary_id")
        diary = Diary.objects.filter(id=diary_id).first()

    diary.title = request.POST.get("title")
    diary.content = request.POST.get("content")
    diary.user_id = 1
    diary.save()

    # updateに遷移
    return render(request, "edit.html", {"diary": diary, "page_title": "Update Diary"})

# class based viewの参考として残しておく
class add(TemplateView):
    template_name = "add.html"