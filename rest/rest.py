import time

from flask import Flask,request
from notify import feishu
from gpt import demo
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route('/json', methods=["POST"])
def json_request():
    d = request.get_data()
    print("get data",d)
    json_d = json.loads(d)
    print(json_d)
    # 最多尝试三次，成功则退出
    out = ""
    for i in range(3):
        try:
            out = demo.GetJsonFromURL(json_d['url'])
            break
        except Exception as e:
            print("error", e)
            # 休眠3秒
            time.sleep(3)
            continue
    fs = feishu.FeiShuBot()
    if out == "":
        fs.send_text(f"获取失败: title: {json_d['title']}, url: {json_d['url']}")
    ret = json.loads(out)
    ret['url'] = json_d['url']
    ret['platform'] = json_d['platform']
    s = json.dumps(ret)
    decoded = bytes(s, 'utf-8').decode('unicode_escape')
    fs.send_card(ret)
    return decoded

def RunRest():
    print("here run rest")
    app.run(debug=True,port=9999)
