import json
import os
from datetime import datetime, timedelta
from io import BufferedReader
from typing import Any, Literal, TypeAlias

import requests
from loguru import logger

TENANT_TOKEN_API = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
USER_ID_API = "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id"
MESSAGE_API = "https://open.feishu.cn/open-apis/im/v1/messages"
UPLOAD_IMAGE_API = "https://open.feishu.cn/open-apis/im/v1/images"
UPLOAD_FILE_API = "https://open.feishu.cn/open-apis/im/v1/files"

APP_ID = "cli_a42d12bb897c900e"
APP_SECRET = "hatd45fhjdQRrB5vtzgYGfvur3p0QnAV"
# open_id of user who will receive the message
OPEN_ID = "oc_57c0d4147cccf01a7d3329ea79066c98"

ENABLE = True if all(
    (APP_ID, APP_SECRET, OPEN_ID)
) else False

if not ENABLE:
    logger.warning(
        f"{APP_ID=} or {APP_SECRET=} is not set, feishu bot is unavailable."
    )

FileStream: TypeAlias = BufferedReader | bytes | bytearray
File: TypeAlias = str | FileStream
FileType: TypeAlias = Literal["opus", "mp4", "pdf", "doc", "xls", "ppt", "stream"]
MsgType: TypeAlias = Literal["text", "image", "audio", "media", "file", "interactive"]


def _post(url: str, token: str = "", **kwargs) -> dict:
    if "headers" not in kwargs:
        kwargs["headers"] = {"Content-Type": "application/json"}
    if token:
        kwargs["headers"]["authorization"] = f"Bearer {token}"
    resp = requests.post(url, **kwargs).json()
    if resp["code"]:
        raise Exception(f"Message failed: {resp['msg']}")
    return resp


class TenantToken:
    def __init__(self) -> None:
        self.token = ""
        self.expire_at = datetime.now()

    def request_token(self):
        resp = _post(
            TENANT_TOKEN_API, json={
                "app_id": APP_ID,
                "app_secret": APP_SECRET
            }
        )
        self.token = resp["tenant_access_token"]
        self.expire_at = timedelta(seconds=resp["expire"]) + datetime.now()

    def __get__(self, instance, owner) -> str:
        if not self.token or self.expire_at < datetime.now():
            self.request_token()
        return self.token

    def __set__(self, instance, value):
        raise AttributeError("TenantToken is read-only")


class FeiShuBot:
    token = TenantToken()

    def __init__(self) -> None:
        if not ENABLE:
            return
        self.user_id = OPEN_ID

    def __getattribute__(self, __name: str) -> Any:
        """Disable all methods when enable is False"""
        if ENABLE:
            return super().__getattribute__(__name)
        if __name == "token":
            return ""

        def wrap(*args, **kwargs):
            logger.warning(f"FeiShuBot is disabled, {__name} is unavailable.")

        return wrap

    def _send_message(self, msg_type: MsgType, content: dict) -> dict:
        # TODO: message card
        return _post(
            MESSAGE_API,
            self.token,
            params={"receive_id_type": "chat_id"},
            json={
                "receive_id": self.user_id,
                "msg_type": msg_type,
                "content": json.dumps(content)
            }
        )

    def send_text(self, msg: str) -> dict:
        """send text message

        Args:
            msg(str): message to be sent
        """
        return self._send_message("text", {"text": msg})

    def send_card(self, message: str, header: str = ""):
        """Send feishu card message, only support markdown format now.

        Refer to https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDM14CM4ATN

        Args:
            message(str): markdown message to be sent
            header(str): card header, default is empty
        """

        title = message["title"]
        summary = message['summary']
        api = message['API']
        score = message["score"]
        time = message["time"]
        url = message["url"]

        # 80+红，60-80黄，60-是绿
        if score >= 80:
            template = "red"
            score = "高"
        elif score >= 60:
            template = "green"
            score = "中"
        else:
            template = "grey"
            score = "低"
        if api == "":
            api = "无"
        else:
            api = api.replace(",", "\n")

        content = {
            "config": {"wide_screen_mode": True},
            "elements": [
                # 暂时去掉@所有人： <at id=all></at>
                {"tag": "div", "text": {"tag": "lark_md", "content": ""}},
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**{title}**"}},
                {"tag": "hr"},
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**公告总结**\n{summary}\n❗️**受影响接口**\n**{api}**"}},

                {"tag": "column_set", "flex_mode": "none", "background_style": "default",
                 "columns": [
                     {"tag": "column", "width": "weighted", "weight": 1, "vertical_align": "top", "elements": [
                         {"tag": "column_set", "flex_mode": "none", "background_style": "grey",
                          "columns": [{"tag": "column", "width": "weighted", "weight": 1, "vertical_align": "top",
                                       "elements": [{"tag": "markdown",
                                                     "content": f"💡 **重要性**\n<font color='{template}'>**{score}**</font>",
                                                     "text_align": "center"}]}
                                      ]}]},

                     {
                         "tag": "column",
                         "width": "weighted",
                         "weight": 1,
                         "vertical_align": "top",
                         "elements": [
                             {
                                 "tag": "column_set",
                                 "flex_mode": "none",
                                 "background_style": "grey",
                                 "columns": [
                                     {"tag": "column", "width": "weighted", "weight": 1, "vertical_align": "top",
                                      "elements": [{"tag": "markdown", "content": f"🕐 **时间**\n{time}",
                                                    "text_align": "center"}]}
                                 ]
                             }
                         ]
                     }]},
                {"tag": "hr"},
                {"tag": "action", "actions": [
                    {"tag": "button", "text": {"tag": "plain_text", "content": "交易所公告链接"}, "type": "primary",
                     "multi_url": {"url": f"{url}"}}]}],
        }
        if header:
            content["header"] = {"title": {"tag": "plain_text", "content": header}, "template": template}
        else:
            content["header"] = {"title": {"tag": "plain_text", "content": "交易所公告信息"}, "template": template}
        self._send_message("interactive", content)


if __name__ == '__main__':
    bot = FeiShuBot()
    # bot.send_text("This is a test message")
    data = {
        "title": "Binance Margin Will Delist the ATA/BUSD, FORTH/BUSD, JST/BUSD, QTUM/BUSD, SUN/BUSD, ZEN/BUSD & ZRX/BUSD Isolated Margin Pairs",
        "summary": "Binance Margin will delist the ATA/BUSD, FORTH/BUSD, JST/BUSD, QTUM/BUSD, SUN/BUSD, ZEN/BUSD and ZRX/BUSD isolated margin pairs. Users are advised to close their positions and transfer their assets from Margin Wallets to Spot Wallets before the cessation of margin trading.",
        "API": "/test1,/test2",
        "score": 90,
        "time": "2023-07-07 04:10",
        "url": "https://www.binance.com/en/support/announcement/binance-margin-will-delist-the-ata-busd-forth-busd-jst-busd-qtum-busd-sun-busd-zen-busd-zrx-busd-isolated-margin-pairs-1b4044db45834ae6b367e12ac776215c"
    }

    keys = data.keys()

    for key in keys:
        print(f"{data[key]}")
    bot.send_card(data, header="交易所公告信息")
