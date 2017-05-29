from flask_wtf import Form,FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,EqualTo,Email,Length
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField

class LoginForm(Form):
    email = StringField('email',validators=[InputRequired(),Email()])
    password = PasswordField('password',validators=[InputRequired()])


class RegisterForm(Form):
    name = StringField('Name',validators=[InputRequired()])
    email = StringField('Email',validators=[InputRequired(),Email(message="Not a valid Email-id")])
    password = PasswordField('Password',validators=[InputRequired(),EqualTo('confirm', message='Passwords must match'), Length(min=8)])
    confirm = PasswordField('Confirm Password',validators=[InputRequired()])

class WriteBlog(FlaskForm):
    title = PageDownField('Title',validators=[InputRequired()])
    content = PageDownField('Content',validators=[InputRequired()])
    submit = SubmitField('Submit')
