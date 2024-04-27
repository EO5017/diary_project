import datetime
import re
from utils import common_utils

from accounts.models import Users

class UserValidate:

    def __init__(self, name, mail_address, password, auth):
        self.name = name
        self.mail_address = mail_address
        self.password = password
        self.auth = auth


    # メールアドレスの検証
    def mail_address_validate(self):
        response = {"status": False, "message": ""}
        pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if self.mail_address == "":
            response["message"] = "メールアドレスを入力してください"
        elif len(self.mail_address) > 200:
            response["message"] = "メールアドレスは200文字以内で入力してください"
        elif not re.match(pattern, self.mail_address):
            response["message"] = "メールアドレスの形式が正しくありません"
        else:
            response["status"] = True
        
        return response

    # 名前の検証
    def name_validate(self):
        response = {"status": False, "message": ""}

        max_length = 100

        # TODO: 4バイト文字を含むかどうかの判定
        common = common_utils.CommonUtils()
        if len(common.remove_4bytes_char(self.name)) != len(self.name):
            response["message"] = "名前に絵文字などの4バイト文字は使用できません"

        if self.name == "":
            response["message"] = "名前を入力してください"
        elif len(self.name) > 100:
            response["message"] = "名前は" + str(max_length) + "文字以内で入力してください"
        else:
            response["status"] = True
        
        return response


    def password_validate(self):
        response = {"status": False, "message": ""}

        max_length = 100
        min_length = 8

        pattern = "^[a-zA-Z0-9]+$"

        if self.password == "":
            response["message"] = "パスワードを入力してください"
        elif len(self.password) < min_length:
            response["message"] = "パスワードは" + str(min_length) + "文字以上で入力してください"
        elif len(self.password) > max_length:
            response["message"] = "パスワードは" + str(max_length) + "文字以内で入力してください"
        elif not re.match(pattern, self.password):
            response["message"] = "パスワードは半角英数字で入力してください"
        else:
            response["status"] = True

        return response
    

    # 特有性の検証
    def unique_validate(self):
        response = {"status": False, "message": ""}

        deplicate_user = Users.objects.filter(mail_address=self.mail_address)
        
        if deplicate_user.exists():
            response["message"] = "このメールアドレスは既に登録されています"
        else:
            response["status"] = True
    
        return response
