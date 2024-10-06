import os

from authlib.integrations.flask_client import OAuth
from flask import Flask, url_for, session, jsonify, render_template

app = Flask(__name__)
app.secret_key = os.urandom(24)


oauth = OAuth(app)
discord = oauth.register(
    name='discord',
    client_id="1079473813936414822",
    client_secret="pdOQZ4h_NcAgq0n6BXAD6iSjejJviqIB",
    access_token_url='https://discord.com/api/oauth2/token',
    authorize_url='https://discord.com/api/oauth2/authorize?client_id=1079473813936414822&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fauthorize%2Fcallback&scope=identify',
    authorize_params=None,
    client_kwargs={'scope': 'identify email'},
    userinfo_endpoint='https://discord.com/api/users/@me',
    redirect_uri="http://195.208.172.233:5000/authorize/callback",
)



@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/data', methods=['POST'])
def index1():
    list = ["321312", "213213"]
    return jsonify(list)

@app.route('/login')
def login():
    discord = oauth.create_client('discord')
    redirect_uri = url_for('authorize', _external=True)
    return discord.authorize_redirect(redirect_uri)

@app.route('/authorize/callback')
def authorize():
    discord = oauth.create_client('discord')
    token = discord.authorize_access_token()
    user = discord.get('https://discord.com/api/users/@me').json()

    session['discord_user'] = user

    return jsonify(user)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
