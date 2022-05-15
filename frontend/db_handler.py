#操作数据库#

import sqlite3


def init_db(sql:str, database:str) -> None:
    """初始化数据库
    :params sql: 初始化SQL语句
    :params database: 数据库路径
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()



def get_db(g, database:str):
    """连接数据库
    :params g: flask.g 是flask 程序全局的一个临时变量,充当者中间媒介的作用,我们可以通过它传递一些数据
    :params database: 数据库路径
    """
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(database)
    return db


database_path = "./data.db"
sql = """
CREATE TABLE USERS(
    id      INTEGER     NOT NULL    PRIMARY KEY AUTOINCREMENT,
    name    TEXT,
    email   TEXT   NOT NULL,
    subtime DATE
)
"""
init_db(sql, database_path)