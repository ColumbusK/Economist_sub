import time
import random
import requests
from modules.tools import paser_ctime, match_email
import logging


class Review:
    def __init__(self, bv = "893986615") -> None:
        self.reply_api = "https://api.bilibili.com/x/v2/reply"
        self.bv = bv
        self.reviews = list()
        # self.pages = self.get_pages()

    def get_page(self, pn=1):
        params = {
            "jsonp":"jsonp", 
            "pn": pn,
            "type": 1,
            "oid": self.bv,
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
        }
        try:
            time.sleep(random.random()*7)
            r = requests.get(url=self.reply_api, params=params, headers=headers)
            print(r.url)
            data = r.json()
            return data
        except Exception as e:
            print(e)

    def get_reviews(self):
        all_review = list()
        pn = 1
        while True:
            try:
                replies = self.get_page(pn=pn)['data']['replies']
            except TypeError:
                print("获取评论失败！订阅信息更新失败！")
                logging.info("获取评论失败！订阅信息更新失败！")
                return all_review
            if len(replies) == 0:
                break
            all_review.extend(replies)
            pn += 1
        self.reviews = all_review
        return all_review
            
    def get_suber_info(self):
        info_list = list()
        reviews = self.get_reviews()
        for review in reviews:
            suber_info = dict()
            username = review['member']['uname']
            email = match_email(review['content']['message'])
            sub_time = paser_ctime(review['ctime'])
            suber_info['username'] = username
            suber_info['email'] = email
            suber_info['sub_time'] = sub_time
            info_list.append(suber_info)
        return info_list


