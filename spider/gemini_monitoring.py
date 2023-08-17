import csv
import logging

import binance
import json
import os
import time

import requests
from bs4 import BeautifulSoup


def read_cvs():
    filename = f"gemini.csv"
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
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Referer': f'https://status.gemini.com/'
    }
    # 使用的代理ip地址
    # proxy = {"https": '127.0.0.1:7890'}
    req = requests.get(url="https://status.gemini.com/#past-incidents", headers=headers)
    # 判断结果200
    if req.status_code != 200:
        print('请求失败', req.reason)
        return None
    # 从html中获取 class=incident-container的数据
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.find_all(class_='incident-container')
    # 遍历items，将数据添加到articles中
    pages = []
    for item in items:
        # 获取url
        url = item.find(class_='incident-title').find('a').get('href')
        # 获取标题
        title = item.find(class_='incident-title').find('a').get_text()
        print(url, title)
        page = {"title": title, "url": "https://status.gemini.com" + url}
        pages.append(page)
    return pages

def save_cvs(articles):
    filename = f"gemini.csv"
    data = []
    for item in articles:
        data.append([item['title'], item['url']])

    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        #writer.writerow(["title", "url")  # 写入CSV文件的标题行
        writer.writerows(data)  # 写入数据行

    print(f"数据已保存到 {filename}")


print('开始Gemini文章爬取')
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
        print('Gemini开始爬取')
        articles = get_items()
        for article in articles:
            # 判断文章是否已经存在
            if article["url"] in read_cvs():
                print('Gemini没有新文章')
                continue
            dd = {"platform":"Gemini", "title":article['title'], "url":article['url']}
            req = requests.post(url="http://127.0.0.1:9999/json",data=json.dumps(dd))
            print(article['title'], article['url'])
        # 保存文章
        save_cvs(articles)
        # 等待指定的时间间隔
        time.sleep(interval)
    except Exception as e:
        print(e)
        time.sleep(1)