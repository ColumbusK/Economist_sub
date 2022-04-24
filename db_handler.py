import json
import os
import re

data_path = './db/user_data.json'

recivers = ["zkzkao@foxmail.com", "zkangzhi4@gmail.com",
            "1485994743@qq.com", "849417410@qq.com"]


def check_path(data_path):
    if not os.path.exists(data_path):
        fp = open(data_path, 'w', encoding='utf-8')
        fp.close


def add_new(mail, data_path):
    with open(data_path, 'r') as fp:
        data = json.load(fp)
        mail_list = list(data.keys())
        print(mail_list)
        if mail not in mail_list:
            data[mail] = []
    with open(data_path, 'w') as fp:
        json.dump(data, fp)


def make_record(mail, date: str, data_path) -> None:
    with open(data_path, 'r') as fp:
        data = json.load(fp)
        mail_list = list(data.keys())
        if mail in mail_list:
            data[mail].append(date)
    with open(data_path, 'w') as fp:
        json.dump(data, fp)


def check_records(mail, date, data_path) -> bool:
    '''检查用户邮箱的发送记录'''
    with open(data_path, 'r') as fp:
        data = json.load(fp)
        mail_list = list(data.keys())
        if mail in mail_list:
            records = data[mail]
            if date in records:
                return True
            else:
                return False


for mail in recivers:
    res = check_records(mail, '2022-03-5', data_path)
    print(res)
