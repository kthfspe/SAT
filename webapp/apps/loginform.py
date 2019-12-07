from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    

    def __init__(self):
        self.loginstatus = False
        self.username = StringField('Username', validators=[DataRequired()])
        self.password = PasswordField('Password')
        self.githubpat = PasswordField('Github PAT')
        self.remember_me = BooleanField('Remember Me')
        self.submit = SubmitField('Sign In')

a = LoginForm() 