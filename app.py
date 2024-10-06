import json
import os

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

login = {
    "213": "123",
    "Date44": "ttt",
    "kot_gay": "21312"
}

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def index1():
    request1 = json.loads(request.data.decode("utf-8"))
    if request1["login"] in login.keys():
        if  request1["password"] == login[request1["login"]]:
            request1["code"] = 200
            session['data'] = request1
            return jsonify(request1)
    return jsonify({"code": 403})

@app.route('/servers', methods=['get'])
def servers():
    try:
        print(session['data'])
        if session["login"] in login.keys():
            if  session["password"] == login[session["login"]]:
                session['data'] = session
                return render_template("servers.html")
    except Exception as e:
        return f"<h1>{e}</h1>"





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
