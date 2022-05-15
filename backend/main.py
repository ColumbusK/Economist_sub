import post
import time_stamp

recivers = [
    "zkzkao@foxmail.com", "zkangzhi4@gmail.com", "1485994743@qq.com",
    "849417410@qq.com", "1462349652@qq.com", "1355373223@qq.com",
    "2083431576@qq.com", "3524697955@qq·com", "1030532529@qq.com",
    "1160387293@qq.com", "xuanfau@qq.com"
]

pdf_path = r"F:\Nutstore\图书馆\报刊\The_economist\TE20220514.pdf"

date = time_stamp.get_preview_date(1)

mail_content = f'您好,新一期的经济学人{date}刊已送达,请查收! 享受阅读,祝您天天好心情!'

for receiver in recivers:
    post.send_pdf_mail(receiver, pdf_path, mail_content=mail_content)
