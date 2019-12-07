from flask import Flask, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from config import Config
import sys

app = Flask(__name__)
app.config.from_object(Config)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    githubpat = PasswordField('Github PAT', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('login.html', form = form)
        else:
            print(form.username)
            return render_template('base.html')
    elif request.method == 'GET':
            return render_template('login.html', form = form)
    print(form.username)


#@app.route('/user/<username>')
#def profile(username):
#    return '{}\'s profile'.format(escape(username))

if __name__ == '__main__':
    # The server is run directly
    app.debug = True
    app.run()
# else: (If imported by another module)