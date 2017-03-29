from flask_wtf import Form
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,EqualTo,Email,Length

class LoginForm(Form):
    email = StringField('email',validators=[InputRequired(),Email()])
    password = PasswordField('password',validators=[InputRequired()])


class RegisterForm(Form):
    name = StringField('Name',validators=[InputRequired()])
    email = StringField('Email',validators=[InputRequired(),Email(message="Not a valid Email-id")])
    password = PasswordField('Password',validators=[InputRequired(),EqualTo('confirm', message='Passwords must match'), Length(min=8)])
    confirm = PasswordField('Confirm Password',validators=[InputRequired()])

#class WriteBlog(Form):
