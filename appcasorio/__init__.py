from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # ajuda a modificar a estrutura do banco de dados à medida que o sistema cresce
from flask_login import LoginManager
import os
from config import Config

appcasorio = Flask(__name__)
appcasorio.config.from_object(Config)
db = SQLAlchemy(appcasorio)
migrate = Migrate(appcasorio, db, render_as_batch=True)
login = LoginManager(appcasorio)
login.login_view = 'login'

def create_app(config_class=Config):
    appcasorio = Flask(__name__)
    appcasorio.config.from_object(config_class)

    db.init_app(appcasorio)
    migrate.init_app(appcasorio, db)
    login.init_app(appcasorio)

    return appcasorio


from appcasorio import routes, models
