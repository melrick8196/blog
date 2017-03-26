from app import db
from datetime import datetime
class Users(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))
    blogs = db.relationship('Blog',backref='users',lazy='dynamic')

    def __init__(self,username,password,name):
        self.username = username
        self.password = password
        self.name = name

class Blog(db.Model):
    __tablename__="blog"
    id = db.Column(db.Integer,primary_key=True)
    blog_id = db.Column(db.Integer)
    blog_title = db.Column(db.String(100))
    blog_content = db.Column(db.Text)
    posted_at = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)
    posted_by = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comments',backref='blog',lazy='dynamic')

    def __init__(self,blog_id,blog_title,blog_content,posted_at,posted_by):
        self.blog_id = blog_id
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

    def __init__(self,blog_id,u_id,commented_at,comment_content):
        self.blog_id = blog_id
        self.u_id = u_id
        self.commented_at = commented_at
        self.comment_content = comment_content

class Tags(db.Model):
    __tablename__="tags"
    id = db.Column(db.Integer,primary_key=True)
    tag_name = db.Column(db.String(50))
    blog_id = db.Column(db.Integer)

    def __init__(self,tag_name,blog_id):
        self.tag_name = tag_name
        self.blog_id = blog_id