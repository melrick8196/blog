from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config.from_object('config')
app.secret_key = 'abcdefghiJKM'
db = SQLAlchemy(app)

from app import views, models
