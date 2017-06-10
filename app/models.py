from app import db
from datetime import datetime
from flask_login import LoginManager, UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    blog = db.relationship('Blog',back_populates='users')


class Blog(db.Model):
    __tablename__="blog"
    id = db.Column(db.Integer,primary_key=True)
    blog_title = db.Column(db.String(100))
    blog_content = db.Column(db.Text)
    posted_at = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)
    posted_by = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comments',lazy='dynamic',back_populates='blog')
    tags = db.relationship('Tags',lazy='dynamic',back_populates='blog')
    users = db.relationship('User',back_populates='blog')


    def __init__(self,blog_title,blog_content,posted_at,posted_by):
        self.blog_title = blog_title
        self.blog_content = blog_content
        self.posted_at = posted_at
        self.posted_by = posted_by

class Comments(db.Model):
    __tablename__="comments"
    id = db.Column(db.Integer,primary_key=True)
    blog_id = db.Column(db.Integer,db.ForeignKey("blog.id"))
    u_id = db.Column(db.String(50))
    commented_at = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)
    comment_content = db.Column(db.Text)
    blog = db.relationship("Blog",back_populates='comments')

    def __init__(self,blog_id,u_id,commented_at,comment_content):
        self.blog_id = blog_id
        self.u_id = u_id
        self.commented_at = commented_at
        self.comment_content = comment_content

class Tags(db.Model):
    __tablename__="tags"
    id = db.Column(db.Integer,primary_key=True)
    tag_name = db.Column(db.String(50))
    blog_id = db.Column(db.Integer,db.ForeignKey("blog.id"))
    blog = db.relationship("Blog",back_populates='tags')

    def __init__(self,tag_name,blog_id):
        self.tag_name = tag_name
        self.blog_id = blog_id
