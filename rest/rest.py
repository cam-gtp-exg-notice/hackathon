from flask import Flask,request,render_template
from flask_socketio import SocketIO, emit
from notify import feishu
from gpt import demo
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
#socketio.init_app(app, cors_allowed_origins="*")

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
    s = json.dumps(ret)
    decoded = bytes(s, 'utf-8').decode('unicode_escape')
    fs = feishu.FeiShuBot()
    fs.send_card(ret)
    return decoded

def RunRest():
    print("here run rest")
    socketio.run(app)
    app.run(debug=True,port=9999)

@app.route('/index')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('message', message, broadcast=True)