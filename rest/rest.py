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
    out = demo.GetJsonFromURL(json_d['url'])
    ret = json.loads(out)
    ret['url'] = json_d['url']
    fs = feishu.FeiShuMessagePusher()
    fs.send_text(json.dumps(ret))
    return json_d

def RunRest():
    print("here run rest")
    app.run(debug=True,port=9999)
