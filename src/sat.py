import sys
from flask import Flask, url_for, render_template, request, redirect
from scripts.gitmanager import GitManager
from scripts import filepath

app = Flask(__name__)

gitman = GitManager()
loginstatus = False
username = ""

@app.route('/buildmodel', methods=['GET', 'POST'])
def buildmodel():
    global loginstatus
    if request.method == 'POST':
        option = request.form['options']
        if option == "github":
            return redirect(url_for('menu'))
        else:
            return render_template('builddatamodel.html', loginstatus = loginstatus)
    elif request.method == 'GET':
        return render_template('builddatamodel.html', loginstatus = loginstatus)

    


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global loginstatus
    error = None
    if request.method == 'POST':
        if gitman.gitlogin(request.form['password']) == True:
            #username = request.form['username']
            loginstatus = True
            return redirect(url_for('buildmodel'))
        else:
            return render_template('login.html', error = "Access Denied. Check your Personal Access Token and your access to repo kthfspe/SA", loginstatus = loginstatus)
    elif request.method == 'GET':
        loginstatus = False
        return render_template('login.html', error=error, loginstatus = False)
        
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    global loginstatus
    return render_template('menu.html', loginstatus = loginstatus)

if __name__ == '__main__':
    # The server is run directly
    app.debug = True
    app.run()
# else: (If imported by another module)