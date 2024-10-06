import json
import os

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

db = sqlite3.connect('data.db')

def create_db():
    cur.execute("CREATE TABLE Users(name UNIQUE, password VARCHAR, role STRING)")


def create_profile(loginUser, passwordUser):
    data = [(loginUser, passwordUser, "user"), ]
    cur.executemany("INSERT INTO Users VALUES(?, ?, ?)", data)
    con.commit()

def get_users():
    cur.execute("SELECT * FROM Users")
    result = cur.fetchone()
    print(result)


if not os.path.exists('Miki.db'):
    con = sqlite3.connect("Miki.db")
    cur = con.cursor()
    create_db()
else:
    con = sqlite3.connect("Miki.db")
    cur = con.cursor()

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

@app.route('/servers', methods=['GET'])
def servers():
    try:
        print(session['data'])
        if session['data']["login"] in login.keys():
            if  session['data']["password"] == login[session['data']["login"]]:
                return render_template("servers.html")
    except Exception as e:
        print(e)
        return f"<h1>403</h1>"

@app.route('/servers', methods=['POST'])
def servers1():
    request1 = json.loads(request.data.decode("utf-8"))

    return jsonify(request1)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
