import json
import os
from http.client import responses

import requests
from authlib.integrations.flask_client import OAuth
from flask import Flask, url_for, session, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def index1():
    request1 = json.loads(request.data.decode("utf-8"))
    print(request1)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
