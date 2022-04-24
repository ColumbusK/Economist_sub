import json
from review import Review

DATABASE = './db/data.json'


def get_data() -> list:
    """获取视频全部评论的信息"""
    review  = Review()
    data = review.get_review_mails()
    return data


def open_database(datebase=DATABASE) -> list:
    """打开数据库获取已有用户数据"""
    with open(datebase, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    return data


def update_database(new_data:list, datebase=DATABASE) -> list:
    """更新数据库"""
    with open(datebase, 'w', encoding='utf-8') as fp:
        json.dump(new_data, fp, ensure_ascii=False)


def update_user_data():
    """根据新数据检查并新增订阅用户"""
    new_data = get_data()
    database_data = open_database()
    add_num = len(new_data) - len(database_data)
    for new in new_data:
        for old in database_data:
            if old["username"] == new["username"]:
                break
        else:
            new["send_record"] = list()
            database_data.append(new)
            print(f"新增用户:{new['username']:30}\t邮箱地址:{new['mail_addr']}")
    with open(DATABASE, 'w', encoding='utf-8') as fp:
        json.dump(database_data, fp, ensure_ascii=False)
        print(f"\033[1;32m >>>>>>:用户数据更新成功,新增用户数 {add_num}:<<<<<< \033[0m")



def new_sent_stamp(date:str) -> None:
    """新增用户订阅记录"""
    data = open_database()
    for item in data:
        item["send_record"].append(date)
    update_database(data)
    print(f"\033[1;32m >>>>>>: 新增用户订阅时间戳成功,日期: {date} :<<<<<< \033[0m")

