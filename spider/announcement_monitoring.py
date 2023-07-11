import csv
import logging
import os

import binance
import json
import time
import requests


# 获取列表的文章信息
def get_all_articles():
    url ='https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageSize=20&pageNo=1'
    headers = {
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Referer': f'https://www.binance.com/zh-CN/support/announcement/'
    }
    # 使用的代理ip地址
    # proxy = {"https": '127.0.0.1:10807'}
    req = requests.get(url=url, headers=headers)
    # 判断结果200
    if req.status_code != 200:
        print('请求失败', req.reason)
        return None
    body = req.text
    bodyJson = json.loads(body)

    return bodyJson['data']['catalogs']

def save_cvs(type, articles):
    filename = f"{type}.csv"
    data = []
    for item in articles:
        data.append([item['title'], item['url'], item['releaseDate']])

    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        #writer.writerow(["title", "url", "releaseDate"])  # 写入CSV文件的标题行
        writer.writerows(data)  # 写入数据行

    print(f"数据已保存到 {filename}")


def read_cvs(type):
    filename = f"{type}.csv"
    # 判断文件是否存在
    if not os.path.exists(filename):
        return []

    with open(filename, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # 读取标题行

        data = []
        for row in reader:
            data.append(row)

    articleNames = []
    for row in data:
        articleNames.append(row[0])

    return articleNames


def latest_articles(type):
    print('--------------------------------')

    existsArticleNames = read_cvs(type)
    articles = []
    for item in all_articles:
        if item['catalogId'] == int(navId):
            articles = item['articles']
    # # 过滤掉已经存在的文章
    articles = list(filter(lambda x: x['title'] not in existsArticleNames, articles))
    if len(articles) == 0:
        print(binance.dict_nav[navId] + '没有新文章')
        return

    articles = binance.generate_article_url(articles)
    save_cvs(type, articles)
    print('--------------------------------')
    return articles


logging.info('开始文章爬取')
# 定时执行的时间间隔（以秒为单位）
interval = 600
while True:
    try:
        # 获取所有类型的文章
        all_articles = get_all_articles()

        for navId in binance.dict_nav.keys():
            type = binance.dict_nav[navId]
            articles = latest_articles(type)
            if articles is None:
                logging.info(binance.dict_nav[navId] + '无新文章')
                continue
            print(binance.dict_nav[navId] + '有新的文章：')
            logging.info(binance.dict_nav[navId] + '有新的文章：')
            for article in articles:
                dd = {"title":article['title'], "url":article['url']}
                req = requests.post(url="http://127.0.0.1:9999/json",data=json.dumps(dd))
                print(article['title'], article['url'], article['releaseDate'])
        # 等待指定的时间间隔
        time.sleep(interval)
    except Exception as e:
        print(e)
        time.sleep(interval)