import imp
import json
import re
import time
import random
import requests
from tools import paser_ctime, match_email


class Review:
    def __init__(self, bv = "893986615") -> None:
        self.reply_api = "https://api.bilibili.com/x/v2/reply/main"
        self.bv = bv
        # self.pages = self.get_pages()

    def get_review(self, _next=1):
        params = {
            "oid": self.bv,
            "type": "1",
            "next": _next
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
        }
        try:

            time.sleep(random.random()*7)
            r = requests.get(url=self.reply_api, params=params, headers=headers)
            data = r.json()
            return data
        except Exception as e:
            print(e)

    def get_pages(self):
        """获取评论总页数信息"""
        while True:
            next_review = self.get_review(_next)
            print(next_review)
            if next_review == pre_review:
                break
            else:
                pre_review = next_review
                _next += 1
        return _next

    def get_reply_infos(self):
        """获取评论信息"""
        reply_infos = []
        _next = 1
        while True:
            before_infos = len(reply_infos)
            data = self.get_review(_next)
            replies = data["data"]["replies"]
            # print(replies)
            if not replies:
                print(">>>:", _next, "评论获取失败")
                break
            for reply in replies:
                # 获取已经添加的用户名列表，用于去重,空间换时间
                mail_list = [item["mail_addr"] for item in reply_infos]

                info = {}
                info["username"] = reply["member"]["uname"]

                message = reply["content"]["message"]
                mail_addr = match_email(message)
                info["message"] = message
                info["mail_addr"] = mail_addr

                _ctime = reply["ctime"]
                info["reply_time"] = paser_ctime(_ctime)

                if mail_addr not in mail_list:
                    reply_infos.append(info)
            after_infos = len(reply_infos)
            # 本次没有再增加新的信息即为最后一页
            if after_infos == before_infos:
                break
            else:
                _next += 1
        return reply_infos

    def get_review_mails(self) -> list:
        """获取评论的邮箱和用户名"""
        replies = self.get_reply_infos()
        name_mail = []
        for reply in replies:
            info = {}
            info["username"] = reply['username']
            info["mail_addr"] = reply['mail_addr']
            name_mail.append(info)
        return name_mail


