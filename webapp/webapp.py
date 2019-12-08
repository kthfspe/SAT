from flask import Flask, url_for, render_template, request, redirect
from config import Config
import sys
from apps import githubinterface

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    # List of apps
    return render_template('menu.html')


# Route for handling the login page logic

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Route to Menu Page if login passed
        if githubinterface.githublogin(request.form['username'],request.form['password']) == True:
            return redirect(url_for('menu'))
        # Route back to login page with error message if login failed
        else:
            return render_template('login.html', error = 'Login Failed')
    elif request.method == 'GET':
        #URL for first call

        #If already logged in, route to menu

        #else route to login page
        return render_template('login.html', error=error)

if __name__ == '__main__':
    # The server is run directly
    app.debug = True
    app.run()
# else: (If imported by another module)