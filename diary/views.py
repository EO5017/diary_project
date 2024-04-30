from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import Diary
from utils import datetime_utils
from utils.diary_contents_validate import DiaryContentsValidate

# 一覧ページ
@login_required
def index(request):
    page_title = "Diary"
    # データベースから全ての日記を取得
    diary_list = Diary.objects.filter(user_id=request.session.get("user_id")).order_by("-write_date")

    # date関連をyyyy-mm-dd形式に変換
    for diary in diary_list:
        wirite_date_dtu = datetime_utils.DatetimeUtils(diary.write_date)
        diary.write_date = wirite_date_dtu.convert_into_yyyy_mm_dd()

    # render関数でテンプレートにデータを渡す
    return render(request, "index.html", {"diary_list": diary_list, "page_title": page_title})

# 鑑賞ページ
@login_required
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

# 新規作成ページ
@login_required
def create(request):
    page_title = "Create Diary"

    dtu = datetime_utils.DatetimeUtils()
    write_date = dtu.convert_into_yyyy_mm_dd()

    return render(request, "edit.html", {"page_title": page_title, "write_date": write_date})

# 編集ページ
@login_required
def edit(request, diary_id):
    page_title = "Update Diary"

    if not diary_id:
        return render(request, "error.html")
    
    user = request.session.get("user_id")
    diary = Diary.objects.filter(id=diary_id , user_id=user).first()

    if not diary:
        return render(request, "error.html")
    
    dtu = datetime_utils.DatetimeUtils(diary.write_date)
    write_date = dtu.convert_into_yyyy_mm_dd()

    return render(request, "edit.html", {"diary": diary, "page_title": page_title, "write_date": write_date})

# 削除
@login_required
def delete(request, diary_id):
    if not diary_id:
        return render(request, "error.html")
    
    user = request.session.get("user_id")

    diary = Diary.objects.filter(id=diary_id , user_id=user).first()
    if not diary:
        return render(request, "error.html")
    
    diary.delete()

    messages.success(request, "削除しました")

    # indexに遷移
    return redirect("index")

# 投稿・更新処理
def post(request):
    title = request.POST.get("title")
    content = request.POST.get("content")

    if not request.POST.get("diary_id"):
        write_date = request.POST.get("write_date")

        validate_response = validate(title, content, write_date)

        for message in validate_response:
            messages.error(request, message)

        page_title = "Create Diary"

        # 新規登録
        diary = Diary()

    else:
        # 更新
        diary_id = request.POST.get("diary_id")
        diary = Diary.objects.filter(id=diary_id).first()
        if not diary:
            return render(request, "error.html")
        
        dtu = datetime_utils.DatetimeUtils(diary.write_date)
        write_date = dtu.convert_into_yyyy_mm_dd()

        validate_response = validate(title, content, write_date, diary_id)

        for message in validate_response:
            messages.error(request, message)

        page_title = "Update Diary"

    if validate_response != []:
        diary = {
            "title": title,
            "content": content,
            "write_date": write_date
        }
        if diary_id:
            diary["id"] = diary_id
        return render(request, "edit.html", {"diary": diary, "page_title": page_title, "write_date": write_date})

    diary.title = title
    diary.content = content
    diary.user_id = request.session.get("user_id")
    diary.write_date = write_date

    diary.save()

    messages.success(request, "保存しました")

    # updateに遷移
    return redirect("edit", diary.id)

# バリデーション
def validate(title, content, write_date, diary_id=None):
    messages = []
    # バリデーション
    validate = DiaryContentsValidate(title, content, write_date, diary_id)
    title_response = validate.title_is_valid()
    content_response = validate.content_is_valid()
    write_date_response = validate.write_date_is_valid()

    if not title_response["status"]:
        for message in title_response["message"]:
            messages.append(message)
    if not content_response["status"]:
        for message in content_response["message"]:
            messages.append(message)
    if not write_date_response["status"]:
        for message in write_date_response["message"]:
            messages.append(message)

    return messages

# class based viewの参考として残しておく
class add(TemplateView):
    template_name = "add.html"
