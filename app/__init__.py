from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask import Flask

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(config['default'])
db.init_app(app)

from . import models

migrate = Migrate()
migrate.init_app(app, db)

