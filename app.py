import json
import os

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import sqlite3

from flask import Flask, render_template, redirect, url_for, flash
from models import db, User
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

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
            flash('You have been logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.route('/login', methods=['POST'])
# async def index1():
#     request1 = json.loads(request.data.decode("utf-8"))
#     if request1["login"] in login.keys():
#         if  request1["password"] == login[request1["login"]]:
#             request1["code"] = 200
#             session['data'] = request1
#             return jsonify(request1)
#     return jsonify({"code": 403})

@app.route('/servers', methods=['GET'])
async def servers():
    return render_template("servers.html")


@app.route('/servers', methods=['POST'])
def servers1():
    request1 = json.loads(request.data.decode("utf-8"))

    return jsonify(request1)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
