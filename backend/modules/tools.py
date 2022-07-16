import time
import re
import datetime
import os


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


class Endpoint:
    """邮件断点发送功能"""

    def __init__(self, first_mail: str, file_path='./endpoint.txt') -> None:
        """初始化记录文件"""
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self.add_point(first_mail)

    def add_point(self, mail: str) -> None:
        """记录最后发送的地址"""
        fp = open(self.file_path, 'w', encoding='utf-8')
        fp.write(mail)
        fp.close()

    def get_point(self) -> str:
        """获取最后发送的邮箱"""
        fp = open(self.file_path, 'r', encoding='utf-8')
        mail = fp.read()
        fp.close()
        return mail

    def remove(self):
        os.remove(self.file_path)
