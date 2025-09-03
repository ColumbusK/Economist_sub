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
            "Cookie": """buvid4=F789E310-F25F-4DAA-92E1-CD7443B55C0B61835-023110315-paGIybps7qzihZ%2F%2BHTI6Cg%3D%3D; buvid_fp_plain=undefined; DedeUserID=13849597; DedeUserID__ckMd5=4237b2eb3e08a806; FEED_LIVE_VERSION=V_HEADER_LIVE_NEW_POP; buvid3=0BA7B189-8D23-8DE5-5AB3-2F94114D5F3A24682infoc; b_nut=1730550124; _uuid=3B53B10DF-9C74-D172-3945-593EA64D810DE25008infoc; rpdid=0zbfVGfY3W|1gCzJVUYL|3z|3w1TjQ7u; home_feed_column=5; browser_resolution=1536-791; LIVE_BUVID=AUTO6717390730107243; PVID=1; is-2022-channel=1; enable_feed_channel=ENABLE; CURRENT_QUALITY=112; SESSDATA=5b65dacb%2C1757647234%2Cd7230%2A32CjBR99QLFGwrWpdK6IYSrkH2dVQNjw6P11MVdJJA3Ck-hxLNeh67bhTWwOg2RUN0yWcSVm94dGlEQk5aUGtWNV91M2hyUWhadEVjck5ER2ROZTlUSExtMGlsTFdYQmQ0MHZ4Qnp4SmhVZFBoaUlTb0RqQkt2dG5RejA2ZFFrcHhfMjVwQmlpdFFnIIEC; bili_jct=fd29a3e664fd86900117356b15e3f523; fingerprint=26cafb97e6e3eac0fbb640cf53888cfb; buvid_fp=abdddcdf807444b075a343cf7e25c6b4; bp_t_offset_13849597=1045238110331338752; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDI0NzgwMTAsImlhdCI6MTc0MjIxODc1MCwicGx0IjotMX0.I0mir-FyuyiysQMUSWaLgwZdQwC2UkFuYMbX48I8kM0; bili_ticket_expires=1742477950; b_lsid=A522399A_195A8DF33CC; bsource=search_google""",
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
        while pn <= 1:
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
