import sqlite3
import traceback
import sys
from modules.review import Review
import os
# 引入
import logging

# 处理路径
cur_dir = os.path.abspath(__file__).rsplit("/", 1)[0]
log_path = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'app.log')

# 1. 创建日志对象
logger = logging.getLogger()
# 2. 日志文件处理
fh = logging.FileHandler(filename=log_path, mode='a', encoding='utf-8')
# 2.1 日志格式
formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(message)s")
# 2.2 应用日志格式
fh.setFormatter(formatter)
# 2.3 添加文件处理
logger.addHandler(fh)

# 3. 日志级别
logger.setLevel(logging.DEBUG)

# 4. 日志输出
logger.debug('This message should go to the log file')
logger.info('So should this')

# logging.basicConfig(filename=log_path, level=logging.DEBUG,
#                     filemode='a', format='%(levelname)s:%(asctime)s:%(message)s', datefmt='%Y-%d-%m %H:%M:%S')
# logging.debug('This message should go to the log file')
# logging.info('So should this')


class SqliteUtil():
    def __init__(self) -> None:
        '''初始化方法，连接数据库'''
        self.database_url = os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), 'suber.db')
        # 连接数据库
        self.db = sqlite3.connect(self.database_url)
        # 设置游标，并将游标设置为字典类型
        self.cursor = self.db.cursor()

    def insert(self, sql):
        '''插入数据库'''
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            # 发生异常则回滚保护数据
            print("insert发生异常", Exception)
            self.db.rollback()
        finally:
            # 最终关闭数据库
            self.db.close()

    def fetchone(self, sql) -> object:
        """查询数据库，返回单个结果集，结果集为对象

        Keyword arguments:
        sql -- SQL查询语句
        Return: 查询结果集
        """
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except:  # 采用traceback模块查看异常
            traceback.print_exc()
            self.db.rollback()
        finally:
            self.db.close()
        return result

    def fetchall(self, sql) -> list:
        """查询数据库，返回多个结果集
        """
        results = None
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:   # 采用sys模块回溯最后的异常
            info = sys.exc_info()
            print(info[0], ':', info[1])
            self.db.rollback()
        finally:
            self.db.close()
        return results

    def delete(self, sql):
        """删除结果集"""
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:   # 异常保存到日志
            fp = open(r'./log.txt', encoding='utf-8')
            traceback.print_exc(file=fp)
            fp.flush()
            fp.close()
            self.db.rollback()
        finally:
            self.db.close()

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        finally:
            self.db.close()


def update_db():
    logging.info("---开始更新订阅用户信息---")
    review = Review()
    suber_info_ls = review.get_suber_info()
    for suber_info in suber_info_ls:
        logging.info(["获取到用户信息", suber_info])
        username = suber_info['username']
        email = suber_info['email']
        sub_time = suber_info['sub_time']
        sql = f'''SELECT * FROM  subers WHERE email="{email}"'''
        db = SqliteUtil()
        res = db.fetchone(sql)
        logging.info(["数据库存在用户信息: ", res])
        # 用户存在则检查更新
        if res:
            if res[1] != username:
                sql = f'''UPDATE subers SET username = '{username}' WHERE suber_id = {res[0]};'''
                logging.info([f"更新用户{res[1]}语句: ", sql])
                db = SqliteUtil()
                db.update(sql)
                sql = f'''SELECT * FROM  subers WHERE email="{email}"'''
                db = SqliteUtil()
                res = db.fetchone(sql)
                logging.info(["更新用户: ", res])
            continue
        sql = f'''INSERT INTO subers(username, email, sub_time) 
    VALUES("{username}","{email}", "{sub_time}");'''
        print("新增用户: ", sql)
        logging.info(["新增用户: ", sql])
        db = SqliteUtil()
        db.insert(sql)


def get_all_suber():
    db = SqliteUtil()
    sql = '''SELECT * FROM subers ORDER BY "sub_time" desc;'''
    res = db.fetchall(sql)
    return res


def make_record(username: str, email: str, magzine_date: str, sent_time: str):
    db = SqliteUtil()
    sql = f'''INSERT INTO sent_records(username, email, magzine_date, sent_time) 
        VALUES("{username}","{email}", "{magzine_date}", "{sent_time}");'''
    db.insert(sql)
