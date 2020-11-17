from datetime import datetime

from flask import Flask

from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes
from app.models import User, Note

db.create_all()
db.session.commit()

user1 = User(first_name='John', last_name='Doe', email='john.doe@gmail.com', pwd='12345678')
user2 = User(first_name='John', last_name='Foo', email='john.foo@gmail.com', pwd='87654321')
db.session.add(user1)
db.session.add(user2)
db.session.commit()
users = User.query.all()
print(users)
