import os

import requests
from authlib.integrations.flask_client import OAuth
from flask import Flask, url_for, session, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/data": {"origins": "http://109.237.99.125:5000"}})
app.secret_key = os.urandom(24)


CLIENT_ID = '1079473813936414822'
CLIENT_SECRET = 'pdOQZ4h_NcAgq0n6BXAD6iSjejJviqIB'
REDIRECT_URI = 'http://109.237.99.125:5000/callback'
DISCORD_OAUTH_URL = 'https://discord.com/api/oauth2/authorize'
DISCORD_TOKEN_URL = 'https://discord.com/api/oauth2/token'
DISCORD_API_URL = 'https://discord.com/api/users/@me'
SCOPE = 'identify'

oauth = OAuth(app)
discord = oauth.register(
    name='discord',
    client_id="1079473813936414822",
    client_secret="pdOQZ4h_NcAgq0n6BXAD6iSjejJviqIB",
    access_token_url='https://discord.com/api/oauth2/token',
    authorize_url='https://discord.com/api/oauth2/authorize',
    authorize_params=None,
    client_kwargs={'scope': 'identify'},
    userinfo_endpoint='https://discord.com/api/users/@me',
    redirect_uri="http://109.237.99.125:5000/callback",
)
@app.route('/login')
def login():
    discord = oauth.create_client('discord')
    redirect_uri = url_for('authorize', _external=True)
    return discord.authorize_redirect(redirect_uri)
@app.route('/callback')
def authorize():
    discord = oauth.create_client('discord')
    token = discord.authorize_access_token()
    user = discord.get('https://discord.com/api/users/@me').json()
    session['discord_user'] = user
    return jsonify(user)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/data', methods=['POST'])
def index1():
    list = ["321312", "213213"]
    return list


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
