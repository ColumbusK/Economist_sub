import yagmail


# 1. 配置SMTP服务
mail_163 = "columbusknight@163.com"
pwd_163 = 'IMZSDHKHDACEZDSY'
smtp_163 = 'smtp.163.com'

# 2. 邮件内容
contents = [f'''你好! 新一期经济学人{"2022/06/25"}刊已送达, 请查收! 享受阅读, 祝你天天好心情! 
  (PS：近期涉及数据库部分重写和smtp服务更换，有时存在附件丢失以及发送失败情况，调整中请多包涵)
  !注意: 请不要将此订阅邮件设为垃圾邮件以免影响服务稳定性！''']

# 3. 实例化SMTP对象
mail = yagmail.SMTP(user=mail_163, password=pwd_163, host=smtp_163)

# 4. send方法发送
subject = "哥伦布骑士的报刊厅(测试2.1)"
receivers = ['zkzkao@foxmail.com', 'zkangzhi4@gmail.com',
             '207067789@qq.com', 'leoliangsz@163.com']
pdf_path = r"F:\Nutstore\图书馆\报刊\The_economist\TE20220625.pdf"

print(contents)
res = mail.send(to=receivers, subject=subject,
                contents=contents, attachments=pdf_path)
print(res)
