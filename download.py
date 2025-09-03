import requests
import re
from PIL import Image
import os
import time


def parser() -> list:
    # 定义文件名
    file_name = "./raw.txt"
    # 存储提取的 contentUrl
    image_urls = []

    # 逐行读取文件并提取 contentUrl
    with open(file_name, "r") as file:
        for line in file:
            match = re.search(r'contentUrl: "([^"]+)"', line)
            if match:
                image_url = (
                    match.group(1).replace("pages", "images").replace("jsonp", "jpg")
                )
                print(image_url)
                image_urls.append(image_url)
    return image_urls


proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}


def download(url: str, folder: str = "./images", file_name: str = "photo.jpg"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
            response.raise_for_status()
            os.makedirs(folder, exist_ok=True)
            with open(f"{folder}/{file_name}.jpg", "wb") as file:
                file.write(response.content)
            print(f"{file_name} 下载成功")
            return
        except requests.exceptions.RequestException as e:
            print(f"下载失败（第 {attempt+1} 次尝试）: {e}")
            time.sleep(2)  # 增加延迟避免触发反爬
    print(f"最终下载失败：{url}")


def jpg_to_pdf(image_folder, output_pdf):
    # 获取指定文件夹中所有 JPG 文件
    image_files = sorted(
        [f for f in os.listdir(image_folder) if f.endswith(".jpg")],
        key=lambda x: int(os.path.splitext(x)[0].split("_")[0]),  # 按页码排序
    )

    # 打开所有图片并转换为 PDF 所需的格式
    images = [
        Image.open(os.path.join(image_folder, img)).convert("RGB")
        for img in image_files
    ]

    # 保存为 PDF，第一张图片作为起始页，其他图片附加
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"PDF 生成成功: {output_pdf}")
    else:
        print("未找到 JPG 文件。")


# 使用示例
# jpg_to_pdf(image_folder="./book", output_pdf="output.pdf")


def main():
    image_urls = parser()
    for idx, image_url in enumerate(image_urls):
        match = re.search(r"_(.*)\.jpg$", image_url)
        file_name = match.group(1) if match else str(idx)
        print(f"正在下载：{file_name}")
        download(image_url, folder="./book", file_name=file_name)
        time.sleep(1)  # 加一秒延迟防止过快请求


main()
