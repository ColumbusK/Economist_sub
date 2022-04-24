import time
import re


def paser_ctime(ctime: int) -> str:
    """时间戳转为格式化时间字符"""
    if type(ctime) == type(1):
        local_time = time.localtime(ctime)
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        return datetime
    print("时间戳不是整数")


def match_email(text: str) -> str:
    """匹配文本中出现的邮箱"""
    pattern = re.compile(r"[\w\d]+@.+\.com")
    mail = re.search(pattern=pattern, string=text)
    if mail:
        mail_addr = mail.group(0)
        return mail_addr


s = "滴！白嫖卡！1160387293@q.com，感谢UP主，不知道还发车嘛"
res = match_email(s)
print(res)