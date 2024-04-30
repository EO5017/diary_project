import datetime
import re
from django.contrib.auth.hashers import make_password, check_password

from accounts.models import Users

class UserExists:

    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def duplication_check(self):
        response = {"status": False, "message": ""}
        user = Users.objects.filter(email=self.email).first()

        if user:
            response["message"] = "ユーザが存在します"
        else:
            response["status"] = True

        return response

    def exist_check(self):
        response = {"status": False, "message": ""}

        user = Users.objects.filter(email=self.email).first()

        if not user:
            response["message"] = f"{self.email}は登録されていません"
        elif not check_password(self.password, user.password):
            response["message"] = "パスワードが違います"
        else:
            response["status"] = True
        
        return response

