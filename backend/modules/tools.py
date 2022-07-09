import time
import re
import datetime


def paser_ctime(ctime: int) -> str:
    """时间戳转为格式化时间字符"""
    if type(ctime) == type(1):
        local_time = time.localtime(ctime)
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        return datetime
    print("时间戳不是整数")


def match_email(text: str) -> str:
    """匹配评论中的邮箱
    Args:
        text (str): 评论文本
    Returns:
        str: 评论中邮箱
    """
    pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]{2,10}\.[a-zA-Z0-9-]+")
    mail = re.search(pattern=pattern, string=text)
    if mail:
        mail_addr = mail.group(0)
        return mail_addr


def get_last_saturday():
    """返回最近周六的日期
    Keyword arguments:
    Return: 日期字符串  "%Y/%m/%d"
    """
    struct = time.localtime()
    weekday = int(time.strftime("%w", struct))
    # print(weekday)
    if weekday == 6:
        days = 0
    elif weekday == 7:
        days = 1
    else:
        days = weekday + 1
    today = datetime.date.today()
    # print(today)
    last_saturday = today - datetime.timedelta(days=days)
    last_saturday = last_saturday.strftime("%Y/%m/%d")
    # print(last_saturday)
    return last_saturday


def get_time_stamp() -> str:
    now = time.localtime()
    stamp = time.strftime("%Y-%m-%d %H:%M:%S", now)
    return stamp
