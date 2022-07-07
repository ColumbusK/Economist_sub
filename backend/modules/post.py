import os
import random
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
import smtplib

import yagmail

Mails = [
    {
        "mail": "zkzkao@foxmail.com",
        "auth": "ptypudtvvhlecajj",
        'smtp': "smtp.qq.com"
    },
    {
        "mail": "2683747644@qq.com",
        "auth": "rewhrnednwjjebig",
        'smtp': "smtp.qq.com"
    },
    {
        "mail": "columbusknight@163.com",
        "auth": "IMZSDHKHDACEZDSY",
        'smtp': "smtp.163.com"
    },
    {
        "mail": "ColumbusK@163.com",
        "auth": "EJXNFEVIVTGFHEFR",
        'smtp': "smtp.163.com"
    },
]


HTML_TEMPLETE = """
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
  </style>
</head>

<body style="width: 100vw; height: 100vh">
  <div style="margin:10px auto; width: 80vw; height: 100%; border: 2px solid #999; overflow:hidden">
    <div style="margin:10px auto; width: 95%">
      <img src="cid:eco_logo" alt="" style="width: 100%; height: 100%">
    </div>
    <div style="margin:10px auto; width: 80%; font-size:medium">
      <p><strong style="color: #ff548c;">Username</strong>, 你好</p>
    </div>
    <div style="margin:10px auto; margin-top: 190px; width: 70%">
      <img src="cid:bili_logo" alt="" srcset="" style="width: 100%; height: 100%">
    </div>
    <h4 style="text-align: center; font-size:medium; color: #05affe">@哥伦布骑士</h4>
  </div>
</body>

</html>
"""


smtp_163 = 'smtp.163.com'
smtp_qq = 'smtp.qq.com'
# 收件人邮箱receiver
receiver = 'zkangzhi4@gmail.com'
# 邮件的正文内容
mail_content = '您新一期的经济学人已送达,请查收! 享受阅读,祝您天天好心情!'
# 邮件标题
mail_title = '哥伦布骑士的报刊厅(测试2.1)'


class Poster():
    def __init__(self, pdf_path: str) -> None:
        self.smtp_service = None
        self.pdf_apart = None
        self.pdf_path = pdf_path
        self.mail_content = "您好, 新一期的经济学人已送达, 请查收! 享受阅读, 祝您天天好心情!"
        self.mail_title = "哥伦布骑士的报刊厅(V2.3)"

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
        print("发件邮箱>>>:", self.smtp_service['mail'])

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
            msg["Subject"] = Header(mail_title, 'utf-8')
            msg["From"] = Header("哥伦布骑士", 'utf-8')
            msg["To"] = receiver
            mail_content = MIMEText(mail_content, "plain", 'utf-8')

            msg.attach(mail_content)
            # 添加pdf附件
            msg.attach(self.pdf_apart)

            # ssl登录
            # smtp = SMTP_SSL(host_server)
            # # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
            # # smtp.set_debuglevel(1)
            # smtp.ehlo(host_server)
            # smtp.login(sender_mail, pwd)
            # smtp.sendmail(sender_mail, receiver, msg.as_string())
            # smtp.quit()
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
        self.load_smtp()
        # 配置SMTP服务
        host_server = self.smtp_service['smtp']
        sender_mail = self.smtp_service['mail']
        pwd = self.smtp_service['auth']

        # 构造邮件
        msg = MIMEMultipart('related')
        msg["Subject"] = Header(self.mail_title, 'utf-8')
        msg["From"] = Header("哥伦布骑士", 'utf-8')
        msg["To"] = receiver
        # 添加pdf附件
        msg.attach(self.pdf_apart)
        # HTML部分
        msgAlternative = MIMEMultipart('alternative')
        msgAlternative.attach(MIMEText(html_content, 'html', 'utf-8'))
        msg.attach(msgAlternative)
        # HTML插图
        fp = open('../resource/TheEco_logo.png', 'rb')
        msgImage1 = MIMEImage(fp.read())
        fp.close()
        fp = open('../resource/Bilibili_Logo.png', 'rb')
        msgImage2 = MIMEImage(fp.read())
        fp.close()
        # 定义图片 ID，在 HTML 文本中引用
        msgImage1.add_header('Content-ID', '<eco_logo>')
        msgImage2.add_header('Content-ID', '<bili_logo>')
        msg.attach(msgImage1)
        msg.attach(msgImage2)
        # 送信状态标志位
        flag = True
        # 送信主流程
        try:
            smtp = smtplib.SMTP_SSL(host=host_server)
            smtp.connect(host=host_server, port=465)
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
