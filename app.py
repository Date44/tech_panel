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
login_manager.login_message = None

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role):
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('index'))  # Переадресация на главную страницу
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/users')
@login_required
@role_required('admin')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.role = request.form['role']
        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for('users'))
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>')
@login_required
@role_required('admin')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
    else:
        flash("User not found.", "danger")
    return redirect(url_for('users'))

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("User added successfully!", "success")
        return redirect(url_for('users'))

    return render_template('add_user.html')


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
@role_required('admin')
def admin():
    return render_template("admin.html")


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
