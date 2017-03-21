import re
from datetime import datetime

from sqlalchemy.orm import synonym
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_login import UserMixin

from app import db, login_manager

EMAIL_REGEX = re.compile(r'^\S+@\S+\.\S+$')
USERNAME_REGEX = re.compile(r'^\S+$')


def check_length(attribute, length):
    """Checks the attribute's length."""
    try:
        return bool(attribute) and len(attribute) <= length
    except:
        return False


class BaseModel:
    """Base for all models, providing save, delete and from_dict methods."""

    def __commit(self):
        """Commits the current db.session, does rollback on failure."""
        from sqlalchemy.exc import IntegrityError
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def delete(self):
        """Deletes this model from the db (through db.session)"""
        db.session.delete(self)
        self.__commit()

    def save(self):
        """Adds this model to the db (through db.session)"""
        db.session.add(self)
        self.__commit()
        return self

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict).save()


class User(UserMixin, db.Model, BaseModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column('username', db.String(64), unique=True)
    _email = db.Column('email', db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    bucket_id = db.relationship('Bucket', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        if self.is_admin:
            return '<Admin {0}>'.format(self.username)
        return '<User {0}>'.format(self.username)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        is_valid_length = check_length(username, 64)
        if not is_valid_length or not bool(USERNAME_REGEX.match(username)):
            raise ValueError('{} is not a valid username'.format(username))
        self._username = username

    username = synonym('_username', descriptor=username)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if not check_length(email, 64) or not bool(EMAIL_REGEX.match(email)):
            raise ValueError('{} is not a valid email address'.format(email))
        self._email = email

    email = synonym('_email', descriptor=email)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        if not bool(password):
            raise ValueError('no password given')

        hashed_password = generate_password_hash(password)
        if not check_length(hashed_password, 128):
            raise ValueError('not a valid password, hash is too long')
        self.password_hash = hashed_password

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def seen(self):
        self.last_seen = datetime.utcnow()
        return self.save()

    def to_dict(self):
        return {
            'username': self.username,
            'user_url': url_for(
                'api.get_user', username=self.username, _external=True
            ),
            'member_since': self.member_since,
            'last_seen': self.last_seen
        }

    def promote_to_admin(self):
        self.is_admin = True
        return self.save()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Bucket(db.Model, BaseModel):
    __tablename__ = 'bucket'
    id = db.Column(db.Integer, primary_key=True)
    bucket_description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=None)
    created_by = db.Column(db.String(64), db.ForeignKey('user.username'))
    bucket_endpoint = db.Column(db.String(64))
    destination_endpoint = db.relationship('Destination', backref='bucket', lazy='dynamic')

    def __init__(self, bucket_description, creator=None,
                 created_at=None):
        self.bucket_description = bucket_description
        self.creator = creator
        self.created_at = created_at or datetime.utcnow()

    def __repr__(self):
        return '<{0} bucket created by {1}>'.format(
            self.bucket_description, self.created_by or 'None')

    def to_dict(self):
        return {
            'bucket_description': self.bucket_description,
            'created_by': self.created_by,
            'created_at': self.created_at,
        }

class Destination(db.Model, BaseModel):
    __tablename__ = 'destination'
    id = db.Column(db.Integer, primary_key=True)
    destination_endpoint = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=None)
    created_by = db.Column(db.String(64), db.ForeignKey('user.username'))
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id'))

    def __repr__(self):
        return '<Destination %r>' % self.destination_endpoint

    def to_dict(self):
        return {
            'destination_endpoint': self.destination_endpoint,
            'created_by': self.created_by,
            'created_at': self.created_at,
        }
