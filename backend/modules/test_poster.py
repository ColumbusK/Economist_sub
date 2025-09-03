import yagmail
from modules.templates import HTML_TEMPLATE


Mails = [
    {
        "mail": "zkzkao@foxmail.com",
        "auth": "gkgrsyhlsjexcabf",
        "smtp": "smtp.qq.com",
        "counts": 0,
    },
]


def send_mail(receivers: str, subject: str, contents: list):
    # 1. 配置SMTP服务
    mail = Mails[0]["mail"]
    pwd = Mails[0]["auth"]
    smtp = Mails[0]["smtp"]

    # 2. 邮件内容
    mail_contents = contents

    # 3. 实例化SMTP对象
    mail = yagmail.SMTP(user=mail, password=pwd, host=smtp)

    # 4. send方法发送
    res = mail.send(
        to=receivers,
        subject=subject,
        contents=mail_contents,
    )
    print(res)
    print(f">>>>>>{receivers} 发送完成! <<<<<<")
    return True


mail_content = HTML_TEMPLATE.replace(r"{{username}}", "User").replace(
    r"{{date}}", "2024"
)

# send_mail("zkzkao@foxmail.com", "哥伦布骑士", [mail_content])
