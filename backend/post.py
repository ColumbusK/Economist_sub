from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import os
import smtplib


# sender_qq为发件人的qq号码
sender_mail = 'zkzkao@foxmail.com'
# pwd为qq邮箱的授权码
pwd = 'hsgwdlvhcpzgbhbd'
# 收件人邮箱receiver
receiver = 'zkangzhi4@gmail.com'
# 邮件的正文内容
mail_content = '您新一期的经济学人已送达,请查收! 享受阅读,祝您天天好心情!'
# 邮件标题
mail_title = '哥伦布骑士的报刊厅(测试)'


def send_pdf_mail(receiver, pdf_path, sender_mail=sender_mail, pwd=pwd,
                  mail_title=mail_title, mail_content=mail_content):
    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
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
        if os.path.exists(pdf_path):
            pdfApart = MIMEApplication(open(pdf_path, 'rb').read())
            pdf_name = pdf_path.split('\\')[-1]
            pdfApart.add_header('Content-Disposition',
                                'attachment', filename=pdf_name)
            msg.attach(pdfApart)

        # ssl登录
        smtp = SMTP_SSL(host_server)
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        # smtp.set_debuglevel(1)
        smtp.ehlo(host_server)
        smtp.login(sender_mail, pwd)
        smtp.sendmail(sender_mail, receiver, msg.as_string())
        smtp.quit()
    except Exception as e:
        print(e)
        ret = False

    if ret:
        print(receiver, "邮件发送成功")
    else:
        print(receiver, "邮件发送失败")
    return ret


def make_recievers(sub_data: str) -> str:
    fp = open(sub_data, 'rt', encoding="utf-8")
    receivers = []
    for line in fp:
        mail_addr, name = line.strip(' \n').split(',')
        receivers.append(f"{name}<{mail_addr}>")
    receivers = ','.join(receivers)
    return receivers


def get_receiver_ls(sub_data: str) -> str:
    fp = open(sub_data, 'rt', encoding="utf-8")
    receivers = []
    for line in fp:
        mail_addr = line.strip(' \n').split(',')[0]
        receivers.append(mail_addr)
    return receivers


def send_paper(pdf_bin, pdf_name, receivers, re_mails, sender_mail=sender_mail, pwd=pwd,
               mail_title=mail_title, mail_content=mail_content):
    # MTA设置，SMTP服务商
    host_server = 'smtp.qq.com'
    res = True
    try:
        # 头部
        msg = MIMEMultipart()
        msg['subject'] = Header(mail_title, "utf-8")
        msg["From"] = f"邮递员派特叔叔{sender_mail}"
        msg["To"] = receivers
        # 正文
        mail_content = MIMEText(mail_content, "plain", "utf-8")
        msg.attach(mail_content)
        # pdf附件
        pdf_att = MIMEApplication(pdf_bin)
        pdf_att.add_header('Content-Disposition',
                           'attachment', filename=pdf_name)
        msg.attach(pdf_att)
        # 发送
        smtp = SMTP_SSL(host_server)
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        # smtp.set_debuglevel(1)
        smtp.ehlo(host_server)
        smtp.login(sender_mail, pwd)
        smtp.sendmail(sender_mail, re_mails, msg.as_string())
        smtp.quit()
    except Exception as e:
        print(e)
        res = False
    if res:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
