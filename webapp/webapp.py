from flask import Flask, url_for, render_template, request
from config import Config
import sys


app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'you-will-never-guess'

# Route for handling the login page logic
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Call githubinterface here

        #If positive route to menu

        #If negative, Please try again
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            return 'Invalid Credentials. Please try again.'
        else:
            return render_template('base.html')
    elif request.method == 'GET':
        #URL for first call

        #If already logged in, route to menu

        #else route to login page
        return render_template('login.html', error=error)

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    # List of apps
    pass

if __name__ == '__main__':
    # The server is run directly
    app.debug = True
    app.run()
# else: (If imported by another module)