import yagmail
from modules.templates import HTML_TEMPLATE


Mails = [
    {
        "mail": "845265098@qq.com",
        "auth": "fzxmdsrrqgmlbaja",
        "smtp": "smtp.qq.com",
        "counts": 0,
    },
]


def send_mail(receivers: str, subject: str, contents: list):
    # 1. 配置SMTP服务
    mail_user = Mails[0]["mail"]
    pwd = Mails[0]["auth"]
    smtp_host = Mails[0]["smtp"]

    # 2. 实例化SMTP对象 (修改此处)
    # 显式添加 port=465 和 smtp_ssl=True
    mail = yagmail.SMTP(
        user=mail_user, password=pwd, host=smtp_host, port=465, smtp_ssl=True
    )

    # 3. 发送邮件
    try:
        res = mail.send(
            to=receivers,
            subject=subject,
            contents=contents,
        )
        print(f">>>>>>{receivers} 发送完成! <<<<<<")
        return True
    except Exception as e:
        print(f"发送失败: {e}")
        return False


mail_content = HTML_TEMPLATE.replace(r"{username}", "User").replace(r"{date}", "2024")

send_mail("zkzkao@foxmail.com", "哥伦布骑士", [mail_content])
