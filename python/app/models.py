from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, login_manager

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    notes = db.relationship("Note", cascade="all, delete", backref='author', lazy='dynamic')

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, pwd={self.password_hash}, " \
               f"first_name={self.first_name}, last_name={self.last_name})>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    edit_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_public = db.Column(db.Boolean, nullable=False)
    uuid = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Note(id={self.id}, title={self.title}, content={self.content}, " \
               f"creation_date={self.creation_date}, edit_date={self.edit_date}, " \
               f"id_user={self.id_user}, is_public={self.is_public}, uuid={self.uuid})>"