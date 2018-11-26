from flask import current_app
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from .import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Permissions:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMENTS = 0x08
    ADMINISTER = 0x80


class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('Users', backref='roles', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permissions.FOLLOW |
                     Permissions.COMMENT |
                     Permissions.WRITE_ARTICLES, True),
            'Moderator': (Permissions.FOLLOW |
                          Permissions.COMMENT |
                          Permissions.WRITE_ARTICLES |
                          Permissions.MODERATE_COMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Roles.query.filter_by(name=r).first()
            if role is None:
                role = Roles(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '\nID:{} Name:{} Permissions:{:08b}'.format(self.id,
                                                           self.name,
                                                           self.permissions)


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Roles.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Roles.query.filter_by(default=True).first()

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

    def can(self, permissions):
        return self.role is not None and \
            self.role.permissions == permissions

    def is_administrator(self):
        return self.can(Permissions.ADMINISTER)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator():
        return False


@login_manager.user_loader
def user_load(user_id):
    return Users.query.get(int(user_id))


login_manager.anonymous_user = AnonymousUser
