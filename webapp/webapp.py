from flask import Flask, url_for, render_template, request, redirect
import sys
from apps import githubinterface

app = Flask(__name__)

loginstatus = False
username = ""

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    global loginstatus
    return render_template('menu.html', loginstatus = loginstatus)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global loginstatus, username
    error = None
    if request.method == 'POST':
        if githubinterface.githublogin(request.form['username'],request.form['password']) == True:
            username = request.form['username']
            loginstatus = True
            return redirect(url_for('menu'))
        else:
            return render_template('login.html', error = 'Login Failed', loginstatus = loginstatus)
    elif request.method == 'GET':
        return render_template('login.html', error=error, loginstatus = False)
        


@app.route('/buildmodel', methods=['GET', 'POST'])
def buildmodel():
    pass


if __name__ == '__main__':
    # The server is run directly
    app.debug = True
    app.run()
# else: (If imported by another module)