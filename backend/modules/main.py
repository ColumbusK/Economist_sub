import os
import time
import random
import logging
from typing import List, Tuple

from jinja2 import Template

from modules.db_handler import get_all_suber, update_db, make_record
from modules.post import Poster
from modules.tools import get_last_saturday, get_time_stamp, Endpoint
from modules.templates import HTML_TEMPLATE
from modules.test_poster import send_mail

# ---------------- 配置 ----------------
PROJECT_ABS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = {
    "pdf_path": r"F:\Nutstore\图书馆\报刊\The_economist\TE20220709.pdf",
    "mail_title": "哥伦布骑士的报刊厅(V3.2)",
    "subject": "哥伦布骑士经济学人",
    "max_retry": 3,
    "min_interval": 2,  # 两次发送的最短间隔 (秒)
    "log_file": "mailer.log",
}

# ---------------- 日志 ----------------
logging.basicConfig(
    filename=CONFIG["log_file"],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# ---------------- 工具函数 ----------------
def render_template(nickname: str, pub_date: str, template_str: str) -> str:
    """渲染邮件模板"""
    print(f"🔍 调试信息 - 用户名: {nickname}, 日期: {pub_date}")

    # 检查模板中是否包含变量
    print(f"🔍 模板包含{{username}}: {'{{username}}' in template_str}")
    print(f"🔍 模板包含{{date}}: {'{{date}}' in template_str}")

    try:
        template = Template(template_str)
        result = template.render(username=nickname, date=pub_date)
        print(f"🔍 渲染后包含用户名: {nickname in result}")
        print(f"🔍 渲染后包含日期: {pub_date in result}")
        return result
    except Exception as e:
        print(f"❌ 模板渲染错误: {e}")
        # 如果Jinja2失败，回退到字符串替换
        return template_str.replace("{{username}}", nickname).replace(
            "{{date}}", pub_date
        )


def load_recipients(mode: str, endpoint: Endpoint, me: Tuple) -> List[Tuple]:
    """加载收件人"""
    if mode == "1":  # 新增
        recipients = update_db()
        # 确保自己始终是第一个
        if me not in recipients:
            recipients.insert(0, me)
        else:
            # 如果自己已在列表中，移除后重新插入到第一位
            recipients = [r for r in recipients if r[2] != me[2]]
            recipients.insert(0, me)
    else:  # 断点模式
        suber_list = get_all_suber()
        last_points = endpoint.get_point()
        for idx, suber in enumerate(suber_list):
            if suber[2] in last_points:
                recipients = suber_list[idx + 1 :]
                break
        else:
            recipients = suber_list

        # 确保自己始终是第一个
        if me not in recipients:
            recipients.insert(0, me)
        else:
            # 如果自己已在列表中，移除后重新插入到第一位
            recipients = [r for r in recipients if r[2] != me[2]]
            recipients.insert(0, me)
    return recipients


def send_to_recipient(
    poster: Poster, recipient: Tuple, pub_date: str, endpoint: Endpoint
) -> bool:
    """单个收件人发送邮件"""
    id_, nickname, mail_addr, *_ = recipient
    if not mail_addr or mail_addr == "None":
        print(f"跳过无效邮箱: {nickname} <{mail_addr}>")
        return True  # 跳过

    mail_content = render_template(nickname, pub_date, HTML_TEMPLATE)

    # 显示接收人信息
    print(f"\n{'='*50}")
    print(f"📧 发送邮件给: {nickname} <{mail_addr}>")
    print(f"📅 期刊日期: {pub_date}")
    print(
        f"📧 当前发送邮箱: {poster.smtp_service['mail'] if poster.smtp_service else '未选择'}"
    )
    print(f"{'='*50}")

    logging.info(f"发送给 {nickname} <{mail_addr}>")
    for attempt in range(1, CONFIG["max_retry"] + 1):
        try:
            res = send_mail(
                receivers=mail_addr,
                subject=CONFIG["subject"],
                contents=[mail_content],
            )
            if res:
                print(f"✅ 发送成功: {nickname} <{mail_addr}>")
                # 记录数据库
                make_record(
                    username=nickname,
                    email=mail_addr,
                    magzine_date=pub_date,
                    sent_time=get_time_stamp(),
                )
                endpoint.add_point(mail_addr)
                return True
        except Exception as e:
            print(f"❌ 第 {attempt} 次尝试失败: {nickname} <{mail_addr}> 错误: {e}")
            logging.error(
                f"第 {attempt} 次尝试失败: {nickname} <{mail_addr}> 错误: {e}"
            )
            poster.load_smtp()
            time.sleep(2)
    print(f"💥 放弃发送: {nickname} <{mail_addr}>")
    return False


def batch_send(
    recipients: List[Tuple], poster: Poster, pub_date: str, endpoint: Endpoint
):
    """批量发送邮件"""
    last_sent = 0
    for idx, recipient in enumerate(recipients, start=1):
        now = time.time()
        # 限速控制
        if now - last_sent < CONFIG["min_interval"]:
            time.sleep(CONFIG["min_interval"] - (now - last_sent))
        success = send_to_recipient(poster, recipient, pub_date, endpoint)
        last_sent = time.time()
        if not success:
            logging.error(f"放弃发送 {recipient}")
        if idx % 20 == 0:  # 每 20 封小憩
            pause = random.uniform(5, 15)
            logging.info(f"批量发送 {idx} 封，休息 {pause:.2f} 秒")
            time.sleep(pause)
    endpoint.remove()


# ---------------- 主函数 ----------------
def main():
    MYSELF_INFO = (
        35,
        "哥伦布骑士",
        "zkzkao@foxmail.com",
        "2032-02-26 15:25:33",
        None,
        None,
    )
    pub_date = get_last_saturday()
    poster = Poster(pdf_path=CONFIG["pdf_path"])
    poster.mail_title = CONFIG["mail_title"]
    poster.pdf_init()

    inp = input("选择发送模式(1: 新增, 2: 断点)>>>:")
    endpoint = Endpoint(MYSELF_INFO[2])
    recipients = load_recipients(inp, endpoint, MYSELF_INFO)

    print("刊数：", pub_date)
    print(f"总收件人数: {len(recipients)}")
    print(f"第一个收件人: {recipients[0][1]} <{recipients[0][2]}>")
    inp = input("是否发送(y/n)>>>:")
    if inp.lower() == "y":
        batch_send(recipients, poster, pub_date, endpoint)
        print("发送完成 ✅")


if __name__ == "__main__":
    main()
