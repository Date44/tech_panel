from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

ROLE_HIERARCHY = {
    'user': 1,
    'editor': 2,
    'admin': 3
}


db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user')

    def has_role(self, role):
        return ROLE_HIERARCHY.get(self.role, 0) >= ROLE_HIERARCHY.get(role, 0)
    
