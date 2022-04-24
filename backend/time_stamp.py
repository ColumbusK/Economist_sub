import datetime
import time


def get_preview_date(num: int) -> str:
    """返回当前日期前num日的日期"""
    year, month, day = time.strftime("%Y %m %d").split(" ")
    if int(day) - num < 10:
        day = int(day) - num
        day = '0' + str(day)
    date = '-'.join([year, month, day])
    return date


date = get_preview_date(1)
print(date)