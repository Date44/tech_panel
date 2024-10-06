import json

from flask import Flask, render_template, redirect, url_for, flash
from flask import request, jsonify
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required

from forms import LoginForm
from models import db, User

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET'])
async def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('servers'))
        else:
            pass
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for(''))


@app.route('/servers', methods=['GET'])
@login_required
async def servers():
    return render_template("servers.html")


@app.route('/servers', methods=['POST'])
def servers1():
    request1 = json.loads(request.data.decode("utf-8"))

    return jsonify(request1)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
