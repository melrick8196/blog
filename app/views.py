from flask import render_template, request, flash, redirect, url_for, session
from app import app, db, lm
from app.models import *
from app.forms import *
from app.auth import *
from functools import wraps
from datetime import datetime
from jinja2 import Markup,escape
from flask_login import login_user, logout_user, current_user, login_required
import markdown
from flask import Markup
import re

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/test')
def test():
    content ="## Test    "
    #content = Markup(content.html)
    return render_template('test.html',content=content)


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('blog'))


@app.route('/',methods=['GET','POST'])
def index():
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In')

@app.route('/blog')
def blog():
    blogposts = Blog.query.order_by(Blog.posted_at.desc()).all()
    return render_template('blog.html',blogs = blogposts)


@app.route('/writeblog',methods=['GET','POST'])
@login_required
def write():
    form = WriteBlog()
    allTags = []
    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        title = title.replace(" ",'-')
        tags = form.tags.data
        tags =re.sub(r'( )+',"",tags)
        tags = tags.split(',')
        for tag in tags:
            allTags.append(tag)
        content = form.content.data
        by = current_user.id
        at = datetime.now()
        blog = Blog(title,content,at,by)
        db.session.add(blog)
        db.session.commit()
        getId = Blog.query.filter_by(blog_title=title).filter_by(posted_by=by)
        blogId = 0
        for idValue in getId:
            blogId = idValue.id
        print allTags
        for tag in allTags:
            t = Tags(tag,blogId)
            db.session.add(t)
        db.session.commit()
        flash("Blog added successfully")
        return render_template('writeblog.html',form=form)
    return render_template('writeblog.html',form=form)

@app.route('/post/<title>')
def post(title):
    post = Blog.query.filter_by(blog_title=title)
    return render_template('post.html',post=post)

@app.route('/tags')
def tags():
    tags = Tags.query.distinct(Tags.tag_name).group_by(Tags.tag_name)
    return render_template('all_tags.html',tags=tags)

@app.route('/tag/<tagName>')
def tagSearch(tagName):
    selectedPosts = Blog.query.filter(Blog.tags.any(tag_name=tagName))
    return render_template('selected_posts.html',selectedPosts = selectedPosts,tagName=tagName)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('test'))
