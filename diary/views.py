from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Diary
from .models import User

# Create your views here.
def index(request):
    # Diaryデータを全て取得
    diary_list = Diary.objects.all()
    # Userデータを全て取得
    user_list = User.objects.all()
    return render(request, "index.html", {"diary_list": diary_list, "user_list": user_list})


# class based viewの参考として残しておく
class add(TemplateView):
    template_name = "add.html"