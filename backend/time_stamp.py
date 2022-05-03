import time


def get_pre_date(num: int) -> str:
    """获取前n日的日期字符串"""
    timeStamp = time.time()
    loss = num * 24 * 60 * 60
    timeStamp -= loss
    dateStamp = time.localtime(timeStamp)
    date = time.strftime(r"%Y/%m/%d", dateStamp)
    print(date)
    return date
