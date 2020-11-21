from datetime import datetime

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import humanfriendly
from flask_redis import FlaskRedis

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)
redis_client = FlaskRedis(app)

from app.models import db, User, Note

db.create_all()
db.session.commit()

from app import routes


@app.context_processor
def utility_processor():
    def human_readable_delta(timestamp):
        return humanfriendly.format_timespan(round((datetime.now() - timestamp).total_seconds()))
    return dict(human_readable_delta=human_readable_delta)
