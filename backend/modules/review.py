import time
import random
import requests
from modules.tools import paser_ctime, match_email
import logging


class Review:
    def __init__(self, bv="893986615") -> None:
        self.reply_api = "https://api.bilibili.com/x/v2/reply"
        self.bv = bv
        self.reviews = list()
        # self.pages = self.get_pages()

    def get_page(self, pn=1):
        params = {
            "jsonp": "jsonp",
            "pn": pn,
            "type": 1,
            "oid": self.bv,
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
            "Cookie": """buvid3=45DA44CD-7863-739C-CBC2-9874275F4C3A35069infoc; b_nut=1754209035; _uuid=D762D101010-1CB8-D211-3147-33B76739CB10A34888infoc; buvid_fp=74c7ffa784115d9eadeb5d80e76eaeb0; enable_web_push=DISABLE; theme-tip-show=SHOWED; rpdid=|(umkmklulk)0J'u~lRk|mukR; theme-avatar-tip-show=SHOWED; theme-switch-show=SHOWED; buvid4=8EB4E2AC-44E3-20FD-3AF6-49E32F5C973F16425-025072010-o8oAp5IH2+wn/SteH4wkt3og8qx2WUm5hc4tCNz3+pFYJZiuQZ6TEXNAGSTMSx5E; LIVE_BUVID=AUTO2217616487358869; home_feed_column=5; DedeUserID=13849597; DedeUserID__ckMd5=4237b2eb3e08a806; CURRENT_QUALITY=100; PVID=1; browser_resolution=1536-791; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzQxNzY1MjksImlhdCI6MTc3MzkxNzI2OSwicGx0IjotMX0.hOvBylab8KnIt37e43vSC9gBVxr_LwPFbIOzCKgXUzE; bili_ticket_expires=1774176469; SESSDATA=60348013%2C1789469331%2C10a82%2A32CjDxe9tCcw5M-Pnnq-Ic6StGc79eOaIoJHAalyklPHXRR08Ss6lqoQ8LKDxbj7Y6WfUSVjFWcWt6bjJJcHB1U2FkWnN6cGowMVNoWDdHbXNIOE00dU9ua1pCRFRqeFNwY2JMMFFzSUlvRWxlWTF6YUpGVTczQ3BfS3hQNDVYTGpsd2UzZnNFQkJnIIEC; bili_jct=cc80eef6d0f229a6910e561b0c3fe033; sid=5zbecedx; bp_t_offset_13849597=1182446952340520960; CURRENT_FNVAL=4048; b_lsid=BF3C28AB_19D14953C91""",
        }
        try:
            time.sleep(random.random() * 7)
            r = requests.get(url=self.reply_api, params=params, headers=headers)
            print(r.url)
            data = r.json()
            # print(data)
            return data
        except Exception as e:
            print(e)

    def get_reviews(self):
        all_review = list()
        pn = 1
        while pn <= 3:
            try:
                replies = self.get_page(pn=pn)["data"]["replies"]
                # print(replies)
                print(len(replies), type(replies))
            except TypeError as error:
                print("获取评论失败！订阅信息更新失败！", error)
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
            username = review["member"]["uname"]
            uid = int(review["member"]["mid"])
            email = match_email(review["content"]["message"])
            sub_time = paser_ctime(review["ctime"])
            suber_info["username"] = username
            suber_info["email"] = email
            suber_info["sub_time"] = sub_time
            suber_info["uid"] = uid
            info_list.append(suber_info)
        return info_list
