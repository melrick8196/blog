from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from flask_login import LoginManager, UserMixin

# from flask.ext.markdown import Markdown

app = Flask(__name__)
# Markdown(app)
pagedown = PageDown(app)

app.config.from_object('config')
app.secret_key = 'abcdefghiJKM'
db = SQLAlchemy(app)
lm = LoginManager(app)

from app import views, models
