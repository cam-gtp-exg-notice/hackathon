from flask import Flask,request
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route('/json', methods=["POST"])
def json_request():
    d = request.get_data()
    print("get data",d)
    json_re = json.loads(d)
    print(json_re)
    return json_re

def RunRest():
    print("here run rest")
    app.run(debug=True,port=9999)