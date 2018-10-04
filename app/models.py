from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .import login_manager


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Passsword is not a redeable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        if self.password_hash is None:
            return False
        else:
            return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def user_load(user_id):
    return Users.query.get(int(user_id))
