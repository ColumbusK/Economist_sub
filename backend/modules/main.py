from modules.db_handler import get_all_suber, update_db, make_record
import os
from modules.post import Poster, batch_send
from modules.tools import match_email, get_last_saturday, get_time_stamp, Endpoint
from modules.templates import HTML_TEMPLATE
import time
import random

PROJECT_ABSOLUTE_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

pdf_path = r"F:\Nutstore\图书馆\报刊\The_economist\TE20220709.pdf"
mail_addr = "zkangzhi4@gmail.com"


def main(pdf_path: str):
    update_db()
    suber_list = get_all_suber()
    first_mail = suber_list[0][2]
    endpoint = Endpoint(first_mail)
    pub_date = get_last_saturday()
    mail_title = '哥伦布骑士的报刊厅(V2.3)'
    content_template = HTML_TEMPLATE
    for suber in suber_list:
        if suber[2] == endpoint.get_point():
            index = suber_list.index(suber)
            suber_list = suber_list[index:]
    print(suber_list)
    print("刊数：", pub_date)
    inp = input("是否发送(y/n)>>>:")
    poster = Poster(pdf_path=pdf_path)
    poster.mail_title = mail_title
    poster.pdf_init()
    if inp in 'yY':
        i = 0
        while i < len(suber_list):
            nickname = suber_list[i][1]
            mail_addr = suber_list[i][2]
            if mail_addr == "None":
                i += 1
                continue
            mail_content = content_template.replace(
                "{{username}}", nickname, 1)
            mail_content = mail_content.replace("{{date}}", pub_date, 1)
            print(f"\n{nickname:-^100}")
            print(nickname, pub_date)
            if mail_addr != 'None':
                print(f"向 “{nickname}” : {mail_addr}发送")
                res = poster.send_html_mail(receiver=mail_addr,
                                            html_content=mail_content)
                print(res)
            time.sleep(random.random() * 10)
            if res:
                i += 1
                # 记录发送时间戳
                time_stamp = get_time_stamp()
                make_record(username=nickname, email=mail_addr,
                            magzine_date=pub_date, sent_time=time_stamp)
                # 增加发送断点
                endpoint.add_point(mail_addr)
                print(f"{nickname:=^100}\n")
            else:         # 发送失败则切换邮箱, 并从失败处更新队列向后发送
                poster.load_smtp()
        endpoint.remove()
