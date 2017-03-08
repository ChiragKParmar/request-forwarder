from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

class ProxyUrl(db.Model):
    __tablename__ = 'proxy'
    id = db.Column(db.Integer, primary_key=True)
    incoming_url = db.Column(db.String(64), unique=True)
    outgoing_url = db.Column(db.String(64))

    def __repr__(self):
        return '<ProxyUrl %r>' % self.incoming_url

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username