import time
import post
import time_stamp

recivers = [
    "zkzkao@foxmail.com", "zkangzhi4@gmail.com", "1485994743@qq.com",
    "849417410@qq.com", "1462349652@qq.com", "1355373223@qq.com",
    "2083431576@qq.com", "3524697955@qq.com", "1030532529@qq.com",
    "1160387293@qq.com", "xuanfau@qq.com", "3260065715@qq.com",
    "chuqiang@ualberta.ca"
]
pdf_path = r"D:\Library\经济学人\TE20220430.pdf"

date = time_stamp.get_pre_date(3)
print(date)
print("请稍后...")
time.sleep(3)

if __name__ == '__main__':
    mail_content = f'您好,新一期的经济学人{date}刊已送达,请查收! 享受阅读,祝您天天好心情!'
    for receiver in recivers:
        post.send_pdf_mail(receiver, pdf_path, mail_content=mail_content)
