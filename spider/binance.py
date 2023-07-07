# coding:utf-8
import json
import os
import time

import requests
from bs4 import BeautifulSoup

dict_nav = {
    '48': 'New Cryptocurrency Listing',
    '49': 'Latest Binance News',
    '50': 'New Fiat Listings',
    '51': 'API Updates',
    '93': 'Latest Activities',
    '128': 'Crypto AirDrop',
    '157': 'Wallet Maintenance Updates',
    '161': 'Delisting'
}


"""
时间戳转日期
"""


def custom_time(timestamp):
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(20160505202854)
    dt = time.strftime("%Y%m%d%H%M%S", time_local)
    return dt

def get_items(url, navId):
    headers = {
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Referer': f'https://www.binance.com/zh-CN/support/announcement/'
    }
    # 使用的代理ip地址
    proxy = {"https": '127.0.0.1:7890'}
    req = requests.get(url=url, headers=headers, proxies=proxy)
    # 判断结果200
    if req.status_code != 200:
        print('请求失败', req.reason)
        return None
    body = req.text
    bodyJson = json.loads(body)

    for item in bodyJson['data']['catalogs']:
        if item['catalogId'] == int(navId):
            return item['articles']

    return None


# 获取列表的文章信息
def get_articles(navId):
    target ='https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageSize=20&pageNo='
    # 新建数组
    articles = []
    for i in range(1, 60):
        url = target + str(i)
        print(url)
        items = get_items(url, navId)
        if items is None or len(items) == 0:
            break
        # 遍历items，将数据添加到articles中
        flag = False
        for item in items:
            # 判断是否是2023年以后的文章
            if item['releaseDate'] < 1672502400000:
                print('已经是2023年以后的文章，不再获取', item['releaseDate'])
                flag = True
                continue
            articles.append(item)
        # 休眠1秒，防止请求太快被禁止访问
        time.sleep(5)
        if flag:
            break
    return articles

# 在get_articles方法返回的数据中多拼接一个文章链接
def generate_article_url(articles):
    for item in articles:
        # 文章生成规则：
        #  https://www.binance.com/en/support/announcement/ + 用-拼接的文章标题+code
        #  例如：https://www.binance.com/en/support/announcement/binance-futures-will-launch-usd%E2%93%A2-m-xvg-perpetual-contract-with-up-to-20x-leverage-673af51d78494b5c945dadba6e5072b3
        # 实现比较丑陋，规则不明确
        item['url'] = 'https://www.binance.com/en/support/announcement/' + str(item['title']).replace('?', '').replace('?', '').replace('#', '').replace('/', '-').replace('(', '').replace(')', '').replace(',', '-').replace(', ', '-').replace('“', '').replace('"', '').replace('\'', '-').replace('’', '-').replace(': ', '-').replace(' & ', '-').replace('!', '').replace(':', '-').replace(' ', '-') + '-' + str(item['code'])
    return articles

# 获取已经保存的文章名
def get_article_names(navId):
    # 获取上一级路径
    path = os.path.abspath(os.path.dirname(os.getcwd())) + '/data-binance' + '/' + dict_nav[navId]
    # 判断文件夹是否存在
    if not os.path.exists(path):
        return []
    files = os.listdir(path)
    articleNames = []
    # 截取第一个 -
    for file in files:
        if file.endswith('.txt'):
            articleName = file.split('-', 1)[1]
            print(articleName)
            articleName = articleName.split('.txt')[0]
            articleNames.append(articleName)
    return articleNames


# 保存到本地
def save_txt(navId, title, txt, releaseDate):
    # 获取上一级路径
    path = os.path.abspath(os.path.dirname(os.getcwd())) + '/data-binance' + '/' + dict_nav[navId]
    # 判断文件夹是否存在，不存在则创建
    if not os.path.exists(path):
        os.makedirs(path)

    # releaseDate转为年月日
    date = custom_time(releaseDate / 1000)
    file = path + '/' + str(date) + '-' + title.replace('/', '') + '.txt'
    # 判断文件是否存在，存在则不创建
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write(txt)
        print('保存成功', file)
    else:
        print('文件已存在', file)

# 传入链接，读取内容
def get_content(article, navId):
    url = article['url']
    print(url)
    # 使用的代理ip地址
    headers = {
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Referer': f'https://www.binance.com/zh-CN/support/announcement/'
    }
    # 使用的代理ip地址
    proxy = {"https": '127.0.0.1:4780'}
    req = requests.get(url=url, headers=headers, proxies=proxy)
    if req.status_code != 200:
        print('请求失败', url, req.reason)
        return None
    body = req.text

    # 创建BeautifulSoup对象，并指定解析器为lxml
    soup = BeautifulSoup(body, 'lxml')

    # 使用find_all方法查找所有class为'abc'的元素
    elements = soup.find_all(class_='css-17pixli')

    # 遍历找到的元素，并输出其内容
    for element in elements:
        # 输出成txt文本
         save_txt(navId, article['title'], element.text, article['releaseDate'])
    time.sleep(5)


if __name__ == "__main__":
    for navId in dict_nav.keys():
        existsArticleNames = get_article_names(navId)
        articles = get_articles(navId)
        # 过滤掉已经存在的文章
        articles = list(filter(lambda x: x['title'].replace('/', '') not in existsArticleNames, articles))
        if len(articles) == 0:
            print(dict_nav[navId] + '没有新文章')
            continue
        articles = generate_article_url(articles)
        for article in articles:
            get_content(article, navId)
