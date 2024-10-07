class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    ROLE_HIERARCHY = {
        'user': 1,
        'editor': 2,
        'admin': 3,
        'root': 4
    }

