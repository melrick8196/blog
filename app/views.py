from flask import render_template, request, flash, redirect, url_for, session
from app import app, db
from app.models import *
from app.forms import *
from functools import wraps
from datetime import datetime
from jinja2 import Markup,escape


@app.route('/',methods=['GET','POST'])
def hello():
    return render_template('index.html')



@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        users = Users.query.filter_by(username=email).all()
        count=0
        for u in users:
            count = count+1
        print count
        if count == 0:
            reg = Users(email,password,name)
            db.session.add(reg)
            db.session.commit()
            flash("User created")
        else:
            flash("User already exists")
    return render_template('register.html',form=form)



@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Users.query.filter_by(username=email).filter_by(password=password)
        c =0
        for u in user:
            c = c+1
        if c ==1:
            session['user'] = email
            return redirect('/landing')
        else:
            return render_template('login.html',form=form,message = "Email or Password incorrect")
    else:
        return render_template('login.html',form=form,message = "Enter credentials")
    return render_template('login.html',form=form,message = "")

@app.route('/blog')
def blog():
    blogposts = Blog.query,order_by(desc(posted_at)).all()
    return render_template('blog.html',blogs = blogposts)
