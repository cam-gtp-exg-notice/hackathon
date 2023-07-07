import requests
import os
import socket
import logging

BOT_TOKEN = '6263148799:AAFfoNLQWuI1iTsA6nyRIHPs2A6BdxlvrCI'
WEBHOOK = f'https://api.telegram.org/bot{BOT_TOKEN}'
CHAT_ID = '-1001958725595'


class TelegramMessagePusher(object):
    def __init__(self, webhook=WEBHOOK, chat_id=CHAT_ID):
        """
        机器人初始化
        :param webhook: telegram机器人webhook地址
        :param chat_id:  发送的group或者channel ID
        """
        super(TelegramMessagePusher, self).__init__()
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.webhook = webhook
        self.chat_id = chat_id

    def send_text(self, text):
        url = f'{WEBHOOK}/sendMessage'

        data = {
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False,
            "disable_notification": False,
            "reply_to_message_id": 0,
            "chat_id": self.chat_id
        }
        resp = requests.post(url, data=data,
                             proxies=dict(http='127.0.0.1:7890', https='127.0.0.1:7890'))
        logging.info('%s, %s, %s', str(CHAT_ID), repr(self))
        tg_response = resp.json()
        logging.info("Telegram response: %s", tg_response)


if __name__ == '__main__':
    message = '这是一个测试：{}在{}环境启动了 {} ({})'.format(os.getlogin(), socket.gethostname(), "test", "wsqigo/test")
    print(TelegramMessagePusher().send_text(message))
