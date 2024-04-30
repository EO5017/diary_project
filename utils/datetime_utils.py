import datetime

class DatetimeUtils:
    def __init__(self, date=None):
        if date is None:
            self.date_data = self.get_now()
        else:
            self.date_data = date

    def convert_into_yyyy_mm_dd(self):
        return (self.date_data).strftime("%Y-%m-%d")
    
    def convert_into_yyyy_mm_dd_hh_mm_ss(self):
        return (self.date_data).strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_now():
        return datetime.datetime.now()