import json
import os

from flask import Flask, render_template, requestm, jsonify, request
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

    return jsonify(request1)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
