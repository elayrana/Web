from flask import current_app
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', index=True)

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

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
