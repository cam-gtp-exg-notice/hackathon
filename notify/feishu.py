import asyncio
import base64
import hashlib
import hmac
import json
import logging
import os
import socket
import time
import aiohttp
from json import JSONDecodeError

import requests

WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/b3eee09e-5d96-4d33-9bb5-494d84fd4066"
SECRET = "fiwreEzBbiCVeTcahmxFpb"
APP_ID = "cli_a1dbc9d87479d00e"
APP_SECRET = "EjMMpzkbqhSD0XMnHwwWPcdjPZUpiGOY"


def is_not_null_and_blank_str(content):
    """
    非空字符串
    :param content: 字符串
    :return: 非空 - True，空 - False
    """
    if content and content.strip():
        return True
    else:
        return False


class FeiShuMessagePusher(object):

    def __init__(self, webhook=WEBHOOK, secret=SECRET, pc_slide=False, fail_notice=False):
        """
        机器人初始化
        :param webhook: 飞书群自定义机器人webhook地址
        :param secret:  机器人安全设置页面勾选“加签”时需要传入的密钥
        :param pc_slide:  消息链接打开方式，默认False为浏览器打开，设置为True时为PC端侧边栏打开
        :param fail_notice:  消息发送失败提醒，默认为False不提醒，开发者可以根据返回的消息发送结果自行判断和处理
        """
        timestamp = int(time.time())
        sign = gen_sign(timestamp, secret)
        super(FeiShuMessagePusher, self).__init__()
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.time_stamp = timestamp
        self.webhook = webhook
        self.sign = sign
        self.pc_slide = pc_slide
        self.fail_notice = fail_notice

    def send_text(self, msg):
        """
        消息类型为text类型
        :param msg: 消息内容
        :return: 返回消息发送结果
        """
        data = {"msg_type": "text"}
        if is_not_null_and_blank_str(msg):  # 传入msg非空
            data["timestamp"] = self.time_stamp
            data["sign"] = self.sign
            data["content"] = {"text": msg}
        else:
            logging.error("text类型，消息内容不能为空！")
            raise ValueError("text类型，消息内容不能为空！")

        logging.debug('text类型：%s' % data)
        return self.post(data)

    def post(self, data):
        """
        发送消息（内容UTF-8编码）
        :param data: 消息数据（字典）
        :return: 返回消息发送结果
        """
        try:
            post_data = json.dumps(data)
            response = requests.post(self.webhook, headers=self.headers, data=post_data)
        except requests.exceptions.HTTPError as exc:
            logging.error("消息发送失败， HTTP error: %d, reason: %s" % (exc.response.status_code, exc.response.reason))
            raise
        except requests.exceptions.ConnectionError:
            logging.error("消息发送失败，HTTP connection error!")
            raise
        except requests.exceptions.Timeout:
            logging.error("消息发送失败，Timeout error!")
            raise
        except requests.exceptions.RequestException:
            logging.error("消息发送失败, Request Exception!")
            raise
        else:
            try:
                result = response.json()
            except JSONDecodeError:
                logging.error("服务器响应异常，状态码：%s，响应内容：%s" % (response.status_code, response.text))
                return {'errcode': 500, 'errmsg': '服务器响应异常'}
            else:
                logging.debug('发送结果：%s' % result)
                # 消息发送失败提醒（errcode 不为 0，表示消息发送异常），默认不提醒，开发者可以根据返回的消息发送结果自行判断和处理
                if self.fail_notice and result.get('errcode', True):
                    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    error_data = {
                        "msgtype": "text",
                        "text": {
                            "content": "[注意-自动通知]飞书机器人消息发送失败，时间：%s，原因：%s，请及时跟进，谢谢!" % (
                                time_now, result['errmsg'] if result.get('errmsg', False) else '未知异常')
                        },
                        "at": {
                            "isAtAll": False
                        }
                    }
                    logging.error("消息发送失败，自动通知：%s" % error_data)
                    requests.post(self.webhook, headers=self.headers, data=json.dumps(error_data))
                return result

    def send_msg_with_at(self, msg, key, value, webhook=WEBHOOK):
        """
        消息类型为post类型, 发送富文本消息，并且@open_id对应的用户
        :param key: "email", "name"
        :param value: key对应的搜索值
        :param msg: 消息内容
        :return: 返回消息发送结果
        """
        self.webhook = webhook
        data = {"msg_type": "post"}
        if is_not_null_and_blank_str(msg):  # 传入msg非空
            open_id = asyncio.get_event_loop().run_until_complete(key_to_open_id(key, value))
            data["timestamp"] = self.time_stamp
            data["sign"] = self.sign
            data["content"] = {
                "post": {
                    "zh_cn": {
                        "title": "CAM",
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": msg + " "
                                },
                                {
                                    "tag": "at",
                                    "user_id": open_id,
                                    "user_name": "tom"
                                }
                            ]
                        ]
                    },
                },
            }
        else:
            logging.error("post类型，消息内容不能为空！")
            raise ValueError("post类型，消息内容不能为空！")

        logging.debug('post类型：%s' % data)
        return self.post(data)


class G:
    token_expire_time = time.time() - 10
    tenant_access_token = ""
    all_users = []
    key_ids_map = {}
    users_update_time = time.time() - 700


async def get_tenant_access_token(api_key=None, api_secret=None):
    if time.time() < G.token_expire_time:
        return G.tenant_access_token
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    headers = {
        "Content-Type": "application/json"
    }
    if api_key is None:
        api_key = APP_ID
    if api_secret is None:
        api_secret = APP_SECRET
    req_body = {
        "app_id": api_key,
        "app_secret": api_secret
    }

    # data = bytes(json.dumps(req_body), encoding='utf8')
    async with aiohttp.ClientSession() as sess:
        async with sess.request(method='POST', url=url, headers=headers, json=req_body) as resp:
            if resp.status == 200:
                result = await resp.json()
                if result.get('code', -1) == 0:
                    access_token = result.get("tenant_access_token", "")
                    expire_in_seconds = result.get("expire", 600)
                    G.token_expire_time = time.time() + expire_in_seconds - 60
                    G.tenant_access_token = access_token
                    return access_token
    return ""


async def get_users(page_token=None):
    url = "https://open.feishu.cn/open-apis/ehr/v1/employees?view=full"

    access_token = await get_tenant_access_token()
    if access_token == '':
        return []
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }
    params = {'page_size': 100}
    if page_token is not None:
        params['page_token'] = page_token
    async with aiohttp.ClientSession() as sess:
        async with sess.request(method='GET', url=url, headers=headers, params=params) as resp:
            if resp.status == 200:
                result = await resp.json()
                if result['code'] == 0:
                    if result['data']['has_more']:
                        more_users, err = await get_users(result['data']['page_token'])
                        if err is None:
                            return result['data']['items'] + more_users, None
                    return result['data']['items'], None
            try:
                error = await resp.json()
                return [], error
            except:
                return [], {'status': resp.status}


async def key_to_open_id(key, value):
    if time.time() - G.users_update_time > 600:
        users, error = await get_users()
        if error is None:
            G.all_users = users
        G.users_update_time = time.time()
    if value in G.key_ids_map:
        return G.key_ids_map.get(value, '')
    for user in G.all_users:
        G.key_ids_map[user['system_fields'][key]] = user['user_id']
    return G.key_ids_map.get(value, '')


def gen_sign(timestamp, secret):
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')

    return sign


if __name__ == '__main__':
    message = '这是一个测试：{}在{}环境启动了 {} ({})'.format(os.getlogin(), socket.gethostname(), "test", "wsqigo/test")
    print(FeiShuMessagePusher().send_msg_with_at(message, "email", "wsqigo@1token.trade"))
    print(FeiShuMessagePusher().send_text(message))
