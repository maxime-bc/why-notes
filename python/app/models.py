from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from app import app
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, index=True, unique=True)
    pwd = db.Column(db.String, nullable=False)
    notes = db.relationship("Note", cascade="all, delete", backref='author', lazy='dynamic')

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, pwd={self.pwd}, " \
               f"first_name={self.first_name}, last_name={self.last_name})>"


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
