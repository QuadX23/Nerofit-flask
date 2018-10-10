import os
from flask import Flask
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#
# engine = create_engine('sqlite:///db_relation.db', echo=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from app import views, models


app.secret_key = os.urandom(12)