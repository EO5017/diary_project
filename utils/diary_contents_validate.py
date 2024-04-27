from utils import common_utils

class DiaryContentsValidate:
    
    def __init__(self, title, content):
        self.content = content
        self.title = title
        self.content_short_limit = 1
        self.content_long_limit = 1000
        self.title_short_limit = 1
        self.title_long_limit = 200

    def content_is_valid(self):
        response = {"status": False, "message": ""}
        
        if not self.__content_long_enough():
            response["message"] = f"本文は{self.content_short_limit}文字以上で入力してください"
            return response
        
        if not self.__content_short_enough():
            response["message"] = f"本文は{self.content_long_limit}文字以下で入力してください"
            return response
        
        if self.__content_has_4bytes_char():
            response["message"] = "本文に絵文字などの4バイト文字は使用できません"
            return response
        
        response["status"] = True
        return response
    
    def title_is_valid(self):
        response = {"status": False, "message": ""}
        
        if not self.__title_long_enough():
            response["message"] = "タイトルを入力してください"
            return response
        
        if not self.__title_short_enough():
            response["message"] = f"タイトルは{self.title_long_limit}文字以下で入力してください"
            return response

        
        response["status"] = True
        return response

    def __content_long_enough(self):
        return len(self.content) >= self.content_short_limit
    
    def __content_short_enough(self):
        return len(self.content) <= self.content_long_limit
    
    def __content_has_4bytes_char(self):
        common = common_utils.CommonUtils()
        return len(common.remove_4bytes_char(self.content)) != len(self.content)
    
    def __title_long_enough(self):
        return len(self.title) >= self.title_short_limit
    
    def __title_short_enough(self):
        return len(self.title) <= self.title_long_limit
