from flask import render_template, request, flash, redirect, url_for, session
from app import app, db
from app.models import *
from functools import wraps
from datetime import datetime
from jinja2 import Markup,escape

@app.route('/hello')
def hello():
    return "hello world"
