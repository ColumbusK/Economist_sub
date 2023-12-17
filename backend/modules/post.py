import os
import random
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
from smtplib import SMTP_SSL
from modules.tools import get_time_stamp

import yagmail

Mails = [
    {
        "mail": "zkzkao@foxmail.com",
        "auth": "kwzdwsqnloihcaic",
        'smtp': "smtp.qq.com",
        'counts': 0
    },
    {
        "mail": "2683747644@qq.com",
        "auth": "rewhrnednwjjebig",
        'smtp': "smtp.qq.com",
        'counts': 0
    },
    {
        "mail": "2326617964@qq.com",
        "auth": "pxljpyegdjkteaja",
        'smtp': "smtp.qq.com",
        'counts': 0
    },
    {
        "mail": "2232565130@qq.com",
        "auth": "ctejvcamfkhediid",
        'smtp': "smtp.qq.com",
        'counts': 0
    },
    {
        "mail": "2232565130@qq.com",
        "auth": "xsuxtrcozrtjebgi",
        'smtp': "smtp.qq.com",
        'counts': 0
    },
    {
        "mail": "2686513920@qq.com",
        "auth": "aekvzjfejwvddgbd",
        'smtp': "smtp.qq.com",
        'counts': 0
    },
    {
        "mail": "columbusknight@163.com",
        "auth": "IMZSDHKHDACEZDSY",
        'smtp': "smtp.163.com",
        'counts': 0
    },
    {
        "mail": "ColumbusK@163.com",
        "auth": "EJXNFEVIVTGFHEFR",
        'smtp': "smtp.163.com",
        'counts': 0
    },

]


class Poster():
    def __init__(self, pdf_path: str) -> None:
        self.smtp_service = None
        self.pdf_apart = None
        self.pdf_path = pdf_path
        self.mail_content = "您好, 新一期的经济学人已送达, 请查收! 享受阅读, 祝您天天好心情!"
        self.mail_title = "哥伦布骑士的报刊厅(V3.0)"

    def pdf_init(self):
        pdf_path = self.pdf_path
        if os.path.exists(pdf_path):
            pdfApart = MIMEApplication(open(pdf_path, 'rb').read())
            pdf_name = pdf_path.split('\\')[-1]
            pdfApart.add_header('Content-Disposition',
                                'attachment', filename=pdf_name)
            self.pdf_apart = pdfApart
            print(">>>>>>>> PDF初始化成功 <<<<<<<<")

    def load_smtp(self):
        """选择smtp服务商"""
        self.smtp_service = random.choice(Mails)
        if self.smtp_service['counts'] > 2:
            Mails.remove(self.smtp_service)
        print("发件邮箱>>>:", self.smtp_service['mail'])

    def format_addr(self, addr: str):
        # 解析邮件地址，以保证邮有别名可以显示
        alias_name, addr = parseaddr(addr)
        # 防止中文问题，进行转码处理，并格式化为str返回
        return formataddr((Header(alias_name, charset="utf-8").encode(),
                           addr.encode("uft-8") if isinstance(addr, unicode) else addr))

    def send_pdf_mail(self, receiver: str, mail_content: str):
        self.load_smtp()
        # 邮箱smtp服务器
        host_server = self.smtp_service['smtp']
        pwd = self.smtp_service['auth']
        sender_mail = self.smtp_service['mail']
        # 邮件内容
        mail_title = self.mail_title
        ret = True
        try:
            # 构造邮件
            msg = MIMEMultipart()
            receiver = self.format_addr(receiver)
            msg["Subject"] = Header(mail_title, 'utf-8')
            print(f"ColumbusK <{sender_mail}>", 'utf-8')
            msg["From"] = Header(f"ColumbusK <{sender_mail}>", 'utf-8')
            msg["To"] = receiver
            mail_content = MIMEText(mail_content, "plain", 'utf-8')

            msg.attach(mail_content)
            # 添加pdf附件
            msg.attach(self.pdf_apart)

            with SMTP_SSL(host=host_server, port=465) as smtp:
                # 登录发邮件服务器
                smtp.login(user=sender_mail, password=pwd)
            # 实际发送、接收邮件配置
                smtp.sendmail(from_addr=sender_mail,
                              to_addrs=receiver, msg=msg.as_string())
                smtp.quit()
        except Exception as e:
            print(e)
            ret = False

        if ret:
            print(receiver, "邮件发送成功 √")
        else:
            print(receiver, "邮件发送失败 ×")
        return ret

    def send_html_mail(self, receiver: str, html_content: str):
        if not receiver:
            print(f'{receiver}: 用户邮箱存在错误!')
            return
        self.load_smtp()
        # 配置SMTP服务
        smtp_server = self.smtp_service['smtp']
        sender_mail = self.smtp_service['mail']
        pwd = self.smtp_service['auth']

        # 构造邮件
        msg = MIMEMultipart('related')
        msg["Subject"] = Header(self.mail_title, 'utf-8')
        print(f"ColumbusK <{sender_mail}>".encode('utf-8'))
        msg["From"] = Header(f"zkz <{sender_mail}>")
        msg["To"] = receiver
        msg["date"] = get_time_stamp()
        # 添加pdf附件
        msg.attach(self.pdf_apart)
        # HTML部分
        msgAlternative = MIMEMultipart('alternative')
        msgAlternative.attach(MIMEText(html_content, 'html', 'utf-8'))
        msg.attach(msgAlternative)
        # HTML插图
        fp = open(r'./resource/TheEco_logo.png', 'rb')
        msgImage1 = MIMEImage(fp.read())
        fp.close()
        fp = open(r'./resource/Bilibili_Logo.png', 'rb')
        msgImage2 = MIMEImage(fp.read())
        fp.close()
        # 定义图片 ID，在 HTML 文本中引用
        msgImage1.add_header('Content-ID', '<image1>')
        msgImage2.add_header('Content-ID', '<image2>')
        msg.attach(msgImage1)
        msg.attach(msgImage2)
        # 送信状态标志位
        flag = True
        # 送信主流程
        try:
            with SMTP_SSL(host=smtp_server, port=465) as smtp:
                # 登录发邮件服务器
                smtp.login(user=sender_mail, password=pwd)
                # 实际发送、接收邮件配置
                smtp.sendmail(from_addr=sender_mail,
                              to_addrs=receiver, msg=msg.as_string())
                smtp.quit()
        except Exception as e:
            print(e)
            flag = False
        if flag:
            print(receiver, "邮件发送成功 √")
        else:
            # 失败SMTP计数
            self.smtp_service['counts'] += 1
            print(receiver, "邮件发送失败 ×")
        return flag


def batch_send(receivers: list, subject: str, contents: list, attachment_path: str):
    # 1. 配置SMTP服务
    mail_163 = "columbusknight@163.com"
    pwd_163 = 'IMZSDHKHDACEZDSY'
    smtp_163 = 'smtp.163.com'

    # 2. 邮件内容
    mail_contents = contents

    # 3. 实例化SMTP对象
    mail = yagmail.SMTP(user=mail_163, password=pwd_163, host=smtp_163)

    # 4. send方法发送
    res = mail.send(to=receivers, subject=subject,
                    contents=mail_contents, attachments=attachment_path)
    print(res)
    print(">>>>>> 批量发送完成! <<<<<<")
