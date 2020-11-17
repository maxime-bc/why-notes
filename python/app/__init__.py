from flask import Flask

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.models import db, User, Note

db.create_all()
db.session.commit()

from app import routes
