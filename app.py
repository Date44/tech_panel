import json
from functools import wraps

from flask import Flask, render_template
from flask import request, redirect, url_for, flash
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import current_user

from forms import LoginForm, RegistrationForm
from models import db, User

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')
db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = None

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated and current_user.role == role:
                return fn(*args, **kwargs)
            else:
                return redirect(url_for('index'))  # Перенаправление на домашнюю страницу
        return decorated_view
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET'])
async def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data, role=request.form.get('role', 'user'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

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

@app.route('/admin')
@role_required('admin')  # Только для администраторов
def admin():
    return "Welcome to the admin page!"


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/servers', methods=['GET', "POST"])
@login_required
async def servers():
    if request.method == 'POST':
        request1 = json.loads(request.data.decode("utf-8"))
    return render_template("servers.html")






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
