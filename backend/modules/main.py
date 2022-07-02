from re import sub
from modules.db_handler import get_all_suber, update_db
import os
from modules.post import Poster, batch_send
from modules.tools import match_email, get_last_saturday
import time
import random

PROJECT_ABSOLUTE_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

pdf_path = r"F:\Nutstore\图书馆\报刊\The_economist\TE20220625.pdf"
mail_addr = "zkangzhi4@gmail.com"


def main():
    update_db()
    suber_list = get_all_suber()
    date = get_last_saturday()
    mail_title = '哥伦布骑士的报刊厅(测试2.0)'
    mail_content = f'''“XXX”你好! 新一期经济学人{date}刊已送达, 请查收! 享受阅读, 祝你天天好心情!
  (PS：近期涉及数据库部分重写和smtp服务更换，有时存在附件丢失以及发送失败情况，调整中请多包涵)
  !注意: 请不要将此订阅邮件设为垃圾邮件以免影响服务稳定性！'''
    print(mail_content)
    print("请检查发送日期")
    receivers = [suber[2] for suber in suber_list if suber[2] != 'None']
    print(receivers)
    for suber in suber_list:
        if suber[2] == "xuanfau@qq.com":
            index = suber_list.index(suber)
            suber_list = suber_list[index:]
    print(suber_list)
    inp = input("是否发送(y/n)>>>:")
    # if inp in 'yY':
    #   batch_send(receivers=receivers, subject=mail_title, contents=[mail_content], attachment_path=pdf_path)
    poster = Poster(pdf_path=pdf_path)
    poster.mail_title = mail_title
    poster.pdf_init()
    if inp in 'yY':
        for suber in suber_list:
            mail_addr = suber[2]
            mail_content = mail_content.replace("XXX", suber[1], 1)
            if mail_addr != 'None':
                print(f"向 “{suber[1]}” : {mail_addr}发送")
                poster.send_pdf_mail(receiver=mail_addr,
                                     mail_content=mail_content)
            time.sleep(random.random() * 10 + random.randint(1, 3))
