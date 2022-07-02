from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import os
import yagmail


# sender_qq为发件人的qq号码
mail_163 = 'columbusknight@163.com'
mail_163_2 = 'ColumbusK@163.com'
mail_qq = 'zkzkao@foxmail.com'
mail_g = 'zkangzhi4@gmail.com'
# pwd为qq邮箱的授权码
pwd_163 = 'IMZSDHKHDACEZDSY'
pwd_163_2 = 'EJXNFEVIVTGFHEFR'
pwd_qq = 'ptypudtvvhlecajj'
pwd_g = 'zkz.googl1258'

smtp_163 = 'smtp.163.com'
smtp_qq = 'smtp.qq.com'
smtp_g = 'smtp.gmail.com'
# 收件人邮箱receiver
receiver = 'zkangzhi4@gmail.com'
# 邮件的正文内容
mail_content = '您新一期的经济学人已送达,请查收! 享受阅读,祝您天天好心情!'
# 邮件标题
mail_title = '哥伦布骑士的报刊厅(测试2.1)'


class Poster():
    def __init__(self, pdf_path: str) -> None:
        self.mail = mail_qq
        self.pwd = pwd_qq
        self.mail_content = "您好, 新一期的经济学人已送达, 请查收! 享受阅读, 祝您天天好心情!"
        self.mail_title = "哥伦布骑士的报刊厅(测试2.1)"
        self.smtp = smtp_qq
        self.pdf_apart = None
        self.pdf_path = pdf_path

    def pdf_init(self):
        pdf_path = self.pdf_path
        if os.path.exists(pdf_path):
            pdfApart = MIMEApplication(open(pdf_path, 'rb').read())
            pdf_name = pdf_path.split('\\')[-1]
            pdfApart.add_header('Content-Disposition',
                                'attachment', filename=pdf_name)
            self.pdf_apart = pdfApart
            print(">>>>>>>> PDF初始化成功 <<<<<<<<")

    def send_pdf_mail(self, receiver: str, mail_content: str):
        # qq邮箱smtp服务器
        host_server = self.smtp
        pwd = self.pwd
        sender_mail = self.mail
        mail_title = self.mail_title
        ret = True
        try:
            # 构造邮件
            msg = MIMEMultipart()
            msg["Subject"] = Header(mail_title, 'utf-8')
            msg["From"] = sender_mail
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
