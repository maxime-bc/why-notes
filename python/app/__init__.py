from flask import Flask
from flask_login import LoginManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.models import db, User, Note

db.create_all()
db.session.commit()

from app import routes