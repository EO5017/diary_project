from accounts.models import Users, UserOperation
from django.contrib.auth.hashers import make_password, check_password

class UserCRUD:

    def create_user(self, email, name, password):
        response = {"status": False, "message": []}
        try:
            auth = 1
            password = self.__convert_password(password)
            user = Users(email=email, name=name, password=password, auth=auth)
            user.save()
            response["status"] = True
            return response
        except:
            response["message"].append("ユーザ登録に失敗しました")
            return response


    def update_password(self, email, password):
        response = {"status": False, "message": []}
        try:
            user = Users.objects.filter(email=email).first()

            if user is None:
                response["message"].append("ユーザが存在しません")
                return response
            
            if check_password(password, user.password):
                response["message"].append("以前と同じパスワードは使用できません")
                return response

            user.password = self.__convert_password(password)
            user.save()
            response["status"] = True
            return response
        except:
            response["message"].append("パスワードの変更に失敗しました")
            return response
    

    def update_name(self, email, name):
        response = {"status": False, "message": []}
        try:
            user = Users.objects.filter(email=email).first()
            user.name = name
            user.save()
            response["status"] = True
            return response
        except:
            response["message"].append("名前の変更に失敗しました")
            return response

    def __convert_password(self, password):
        return make_password(password)
