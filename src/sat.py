import sys
import os
sys.path.insert(0,os.getcwd()+"/scripts")
from flask import Flask, url_for, render_template, request, redirect
from gitmanager import GitManager
from datamanager import DataManager
from dbmanager import DBManager
from localfile import readdrawiofile
# from scripts.usermanager import UserManager
import filepath

# Create Flask App object
app = Flask(__name__)

# Create git object to interface to Github
gitman = GitManager()
dataman = DataManager()
loginstatus = False

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global loginstatus
    error = None
    if request.method == 'POST':
        if gitman.gitlogin(request.form['password']) == True:
            loginstatus = True
            return redirect(url_for('buildmodel'))
        else:
            error = "Access Denied. Check your Personal Access Token and your access to repo kthfspe/SA"
            return render_template('login.html', error = error, loginstatus = loginstatus)
    elif request.method == 'GET':
        loginstatus = False
        return render_template('login.html', error=error, loginstatus = False)

@app.route('/buildmodel', methods=['GET', 'POST'])
def buildmodel():
    global loginstatus
    raw_functional = []
    raw_physical = []
    if request.method == 'POST':
        option = request.form['options']
        if option == "github":
            # Read each file from github
            raw_functional1 = gitman.readfile(filepath.defaultLVfun)
            raw_functional2 = gitman.readfile(filepath.defaultHVfun)
            raw_functional3 = gitman.readfile(filepath.defaultDVfun)
            raw_functional = raw_functional1 + raw_functional2 + raw_functional3
            raw_physical1 = gitman.readfile(filepath.defaultLVphy)
            raw_physical2 = gitman.readfile(filepath.defaultHVphy)
            raw_physical3 = gitman.readfile(filepath.defaultDVphy)
            raw_physical = raw_physical1 + raw_physical2 + raw_physical3       
        else:
            # Read file path from user
            path = request.form['localpath']
            # Read each drawio file locally
            raw_functional1 = readdrawiofile(filepath.defaultLVfun)
            raw_functional2 = readdrawiofile(filepath.defaultHVfun)
            raw_functional3 = readdrawiofile(filepath.defaultDVfun)
            raw_functional = raw_functional1 + raw_functional2 + raw_functional3
            raw_physical1 = readdrawiofile(filepath.defaultLVphy)
            raw_physical2 = readdrawiofile(filepath.defaultHVphy)
            raw_physical3 = readdrawiofile(filepath.defaultDVphy)
            raw_physical = raw_physical1 + raw_physical2 + raw_physical3      

        # Build data model using the raw data
        # status, errors, warnings = dataman.buildmodel(raw_physical, raw_functional)

        # Display errors, warnings

        return render_template('output.html', loginstatus = loginstatus)

        # Save errors, warnings to log file

        # Redirect to build model page : return render_template('builddatamodel.html', loginstatus = loginstatus)

        # OR

        # Create DB

        # Display success message

        # Redirect to apps page : return redirect(url_for('menu'))  
        
    elif request.method == 'GET':
        return render_template('builddatamodel.html', loginstatus = loginstatus)


@app.route('/output', methods=['POST','GET'])
def output():
    global loginstatus
    return render_template('output.html', loginstatus = loginstatus)

@app.route('/error', methods=['POST','GET'])
def error():
    global loginstatus
    return render_template('error.html', loginstatus = loginstatus)

@app.route('/warning', methods=['POST','GET'])
def warning():
    global loginstatus
    return render_template('warning.html', loginstatus = loginstatus)

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    global loginstatus
    return render_template('menu.html', loginstatus = loginstatus)

if __name__ == '__main__':
    # The server is run directly
    app.debug = True
    app.run()
# else: (If imported by another module)