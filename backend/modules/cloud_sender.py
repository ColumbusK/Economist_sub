#!/usr/bin/python
# coding:utf-8
import requests

# SendCloud API 配置
API_URL = "https://api.sendcloud.net/apiv2/mail/send"
API_USER = "sc_hvv7xj_test_pTG9kI"
API_KEY = "8817a2cc3b29f67d5f03172242fe7c9f"
FROM_EMAIL = "service@sendcloud.im"
FROM_NAME = "书集@哥伦布骑士"
SUBJECT = "书集网站地址告知邮件"


def send_email(to_email: str, html_content: str):
    """
    发送邮件工具函数

    参数:
        to_email: 收件邮箱地址
        html_content: HTML 格式的邮件内容

    返回:
        requests.Response: API 响应对象
    """
    params = {
        "apiUser": API_USER,
        "apiKey": API_KEY,
        "from": FROM_EMAIL,
        "fromName": FROM_NAME,
        "to": to_email,
        "subject": SUBJECT,
        "html": html_content,
    }

    response = requests.post(API_URL, files={}, data=params)
    return response
