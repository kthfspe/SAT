from flask import render_template
from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect
import requests
from flask_github import GitHub

github = GitHub(app)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login')
@app.route('/login', methods=['GET', 'POST'])
def login():
    return github.authorize()
    PARAMS = {'client_id':"14752ee16c6d1630fe01", 'redirect_uri':'http://localhost:5000','login':'hari195','scope':'','state':'', 'allow_signup':''} 
    r = requests.get(url = "https://github.com/login/oauth/authorize", params = PARAMS) 
    print(PARAMS)
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/github-callback')
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    user = User.query.filter_by(github_access_token=oauth_token).first()
    if user is None:
        user = User(oauth_token)
        db_session.add(user)

    user.github_access_token = oauth_token
    db_session.commit()
    return('/index')