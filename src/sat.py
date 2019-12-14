import sys
from flask import Flask, url_for, render_template, request, redirect
from scripts.gitmanager import GitManager

app = Flask(__name__)

gitman = GitManager()
loginstatus = False
username = ""

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    global loginstatus
    return render_template('menu.html', loginstatus = loginstatus)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global loginstatus, username, gitman
    error = None
    if request.method == 'POST':
        if gitman.gitlogin(request.form['password']) == True:
            #username = request.form['username']
            loginstatus = True
            return redirect(url_for('menu'))
        else:
            return render_template('login.html', error = 'Login Failed', loginstatus = loginstatus)
    elif request.method == 'GET':
        return render_template('login.html', error=error, loginstatus = False)
        


@app.route('/buildmodel', methods=['GET', 'POST'])
def buildmodel():
    global loginstatus
    return render_template('builddatamodel.html', loginstatus = loginstatus)


if __name__ == '__main__':
    # The server is run directly
    app.debug = True
    app.run()
# else: (If imported by another module)