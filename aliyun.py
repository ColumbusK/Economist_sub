from aligo import Aligo
import time


pub_date = time.strftime("%Y%m%d")
print(pub_date)

if __name__ == '__main__':
    ali = Aligo()
    user = ali.get_user()  # 获取用户信息
    ll = ali.get_file_list()  # 获取网盘根目录文件列表
    # 遍历文件列表
    economist_folder = ali.get_file_list("61ffcfdfcdb6fe7e4a874d18b7c6e1b54c3b7acf")
    for file in economist_folder:
        # print(file.file_id, file.name, file.type)
        print(file.name, type(file.name))
        if file.name == pub_date:
            folder = ali.get_file_list(file.file_id)
            print(folder)
            print('--------', file.name)
            ali.download_file("https://www.aliyundrive.com/s/Ltz6aRYhNvK")