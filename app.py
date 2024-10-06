import os

import requests
from flask import Flask, jsonify, render_template, request, redirect
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)


CLIENT_ID = '1079473813936414822'
CLIENT_SECRET = 'pdOQZ4h_NcAgq0n6BXAD6iSjejJviqIB'
REDIRECT_URI = 'http://109.237.99.125:5000/callback'
DISCORD_OAUTH_URL = 'https://discord.com/api/oauth2/authorize'
DISCORD_TOKEN_URL = 'https://discord.com/api/oauth2/token'
DISCORD_API_URL = 'https://discord.com/api/users/@me'
SCOPE = 'identify'

@app.route('/login', methods=['POST'])
def login():
    return redirect(f"{DISCORD_OAUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={SCOPE}")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(DISCORD_TOKEN_URL, data=data, headers=headers)
    r_json = r.json()
    access_token = r_json['access_token']

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    user_info = requests.get(DISCORD_API_URL, headers=headers).json()
    print(user_info)
    return f"Hello, {user_info['username']}#{user_info['discriminator']}! Your email is {user_info['email']}"


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/data', methods=['POST'])
def index1():
    list = ["321312", "213213"]
    return list


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
