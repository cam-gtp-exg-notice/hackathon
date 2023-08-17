import csv
import logging

import binance
import json
import os
import time

import requests
from bs4 import BeautifulSoup


def read_cvs():
    filename = f"mltech.csv"
    # 判断文件是否存在
    if not os.path.exists(filename):
        return []

    with open(filename, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        # headers = next(reader)  # 读取标题行
        data = []
        for row in reader:
            data.append(row)

    urls = []
    for row in data:
        urls.append(row[1])

    return urls


def get_items():
    headers = {
        # 'User - Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Referer': f'https://mltech.ai/'
    }
    # 使用的代理ip地址
    proxy = {"https": '127.0.0.1:7890'}
    req = requests.get(url="https://mltech.ai/blog", headers=headers, proxies=proxy)
    # 判断结果200
    if req.status_code != 200:
        print('请求失败', req.reason)
        return None
    # 从html中获取 class=incident-container的数据
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.find_all(class_='post-last-title')
    # 遍历items，将数据添加到articles中
    articles = []
    for item in items:
        # 获取url
        url = item.find('a').get('href')
        # 获取标题
        title = item.find('a').get_text()
        print(url, title)
        page = {"title": title, "url": url}
        articles.append(page)
    return articles

def save_cvs(articles):
    filename = f"mltech.csv"
    data = []
    for item in articles:
        data.append([item['title'], item['url']])

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        #writer.writerow(["title", "url")  # 写入CSV文件的标题行
        writer.writerows(data)  # 写入数据行

    print(f"数据已保存到 {filename}")


print('开始Mltech文章爬取')
# 定时执行的时间间隔（以秒为单位）
interval = 600

isFirst = True

while True:
    try:
        if isFirst:
            # 初次启动时，先获取一次所有文章
            # 因为请求url容易报错，所以放到while中
            articles = get_items()
            save_cvs(articles)
            isFirst = False
        print('Mltech开始爬取')
        articles = get_items()
        for article in articles:
            # 判断文章是否已经存在
            if article["url"] in read_cvs():
                print('Mltech没有新文章')
                continue
            dd = {"platform":"Mltech", "title":article['title'], "url":article['url']}
            req = requests.post(url="http://127.0.0.1:9999/json",data=json.dumps(dd))
            print(article['title'], article['url'])
        # 保存文章
        save_cvs(articles)
        # 等待指定的时间间隔
        time.sleep(interval)
    except Exception as e:
        print(e)
        time.sleep(10)
