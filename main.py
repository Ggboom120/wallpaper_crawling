import os
import time
import requests
import random
from requests.exceptions import SSLError
from lxml import etree
from tqdm import tqdm

save_path = ""  # 储存路径
start_page = 1  # 起始页数
end_page = 2  # 结束页数

total_files = 0

for page in range(start_page, end_page + 1):
    url = f"https://wallhaven.cc/latest?page={page}"
    response = requests.get(url)
    html = response.text
    tree = etree.HTML(html)
    urls = tree.xpath('//img[contains(@class, "lazyload")]/@data-src')

    for url in urls:
        if url.startswith("https://th.wallhaven.cc/small"):
            filename = url.split("/")[-1]
            new_filename = "wallhaven-" + filename
            new_url = url.replace("https://th.wallhaven.cc/small", "https://w.wallhaven.cc/full").replace(filename, new_filename)
            save_file_path = os.path.join(save_path, filename)
            if os.path.exists(save_file_path):
                print(f"文件已存在，跳过下载：{filename}")
                continue
            try:
                response = requests.get(new_url, stream=True)
                if response.status_code != 404:
                    total_size = int(response.headers.get("content-length", 0))
                    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)
                    with open(save_file_path, "wb") as file:
                        for data in response.iter_content(chunk_size=1024):
                            file.write(data)
                            progress_bar.update(len(data))
                    progress_bar.close()
                    total_files += 1
                    print(f"已保存文件：{filename}")
                    sleep_time = random.uniform(3, 15)
                    print('随机延迟:', sleep_time, '秒')
                    time.sleep(sleep_time)
                else:
                    new_url = new_url.replace(".jpg", ".png")
                    response = requests.get(new_url, stream=True)
                    total_size = int(response.headers.get("content-length", 0))
                    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)
                    with open(save_file_path, "wb") as file:
                        for data in response.iter_content(chunk_size=1024):
                            file.write(data)
                            progress_bar.update(len(data))
                    progress_bar.close()
                    total_files += 1
                    print(f"已保存文件：{filename}")
                    sleep_time = random.uniform(3, 15)
                    print('随机延迟:', sleep_time, '秒')
                    time.sleep(sleep_time)
            except SSLError as e:
                print(f"下载文件时发生SSLError异常：{e}")
                continue

print(f"共下载了 {total_files} 个文件")
