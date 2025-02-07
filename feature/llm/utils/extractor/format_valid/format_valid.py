from datetime import datetime
import re

# ---------邏輯函式----------------------------------

def is_float(value:any) -> bool:
    '''
    判斷是否為浮點數
    '''
    try:
        float(value)
        return True
    except :
        return False

def is_valid_24_hour_time(time_str:str) -> bool:
    '''
    判斷是否為 24 小時制
    '''
    try :
        pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d|24:00$"
        return re.fullmatch(pattern, time_str) is not None
    except :
        return False

def is_valid_mm_dd(date_str: str) -> bool:
    '''
    判斷是否為日期格式
    '''
    try:
        datetime.strptime(date_str, "%m-%d")
        return True
    except :
        return False
