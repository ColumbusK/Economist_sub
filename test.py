import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
import os

sender = 'zkzkao@foxmail.com'
# 接收邮件，可设置为你的QQ邮箱或者其他邮箱
receivers = ['3459068367@qq.com']

msgRoot = MIMEMultipart('related')
msgRoot['From'] = Header("哥伦布骑士", 'utf-8')
msgRoot['To'] = Header(receivers[0], 'utf-8')
msgRoot['Subject'] = Header('哥伦布骑士的报刊厅(V2.3)', 'utf-8')

msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

mail_template = """
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
  <div style="margin:10px auto; width: 375px; height: auto; border: 2px solid #999; overflow:hidden">
    <div style="margin:10px auto; width: 95%">
      <img src="cid:image1" alt="" style="width: 100%; height: 100%">
    </div>
    <div style="margin:10px auto; width: 80%; font-size:medium">
      <p><strong style="color: #ff548c;">{username}</strong>，你好。 新一期经济学人{date}刊已送达, 请查收! 享受阅读, 祝你天天好心情!
  (PS：近期涉及数据库部分重写和smtp服务更换，有时存在附件丢失以及发送失败情况，调整中请多包涵)
  !注意: 请不要将此订阅邮件设为垃圾邮件以免影响服务稳定性！</p>
    </div>
    <div style="margin:0 auto; margin-top: 90px; width: 50%">
      <img src="cid:image2" alt="" srcset="" style="width: 100%; height: 100%">
    </div>
    <h4 style="margin-bottom: 20px; text-align: center; font-size:medium; color: #05affe">@哥伦布骑士</h4>
  </div>
</body>

</html>
"""
mail_msg = mail_template.replace("{username}", '哥伦布骑士', 1)
msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

# 指定图片为当前目录
fp = open('./backend/resource/TheEco_logo.png', 'rb')
msgImage1 = MIMEImage(fp.read())
fp.close()

# 定义图片 ID，在 HTML 文本中引用
msgImage1.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage1)

# 指定图片为当前目录
fp = open('./backend/resource/Bilibili_Logo.png', 'rb')
msgImage2 = MIMEImage(fp.read())
fp.close()

# 定义图片 ID，在 HTML 文本中引用
msgImage2.add_header('Content-ID', '<image2>')
msgRoot.attach(msgImage2)
email = {
    "mail": "zkzkao@foxmail.com",
    "auth": "ptypudtvvhlecajj",
    'smtp': "smtp.qq.com"
}

pdf_path = r"F:\Nutstore\图书馆\报刊\The_economist\TE20220702.pdf"
if os.path.exists(pdf_path):
    pdfApart = MIMEApplication(open(pdf_path, 'rb').read())
    pdf_name = pdf_path.split('\\')[-1]
    pdfApart.add_header('Content-Disposition',
                        'attachment', filename=pdf_name)
    msgRoot.attach(pdfApart)

try:
    email_user = email['mail']
    email_pwd = email['auth']
    mail_host = email['smtp']
    mail_port = 465

    smtp = smtplib.SMTP_SSL(mail_host)
    smtp.connect(mail_host, mail_port)
    smtp.login(email_user, email_pwd)
    smtp.sendmail(sender, receivers, msgRoot.as_string())
    smtp.quit()
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
