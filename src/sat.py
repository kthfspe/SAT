import sys
import os
from flask import Flask, url_for, render_template, request, redirect
from scripts.gitmanager import GitManager
# from scripts.datamanager import datamanager
# from scripts.usermanager import UserManager
from scripts import filepath

# Create Flask App object
app = Flask(__name__)

# Create git object to interface to Github
gitman = GitManager()
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
    if request.method == 'POST':
        option = request.form['options']
        if option == "github":
            #Setup file paths

            # Read each file from github
            # status, rawfilename =loaddb(gitman, parentdir)

            a = gitman.readfile(filepath.defaultLVfun)
            print(type(a[len(a)-1]['BlockType']))
            print(os.getcwd())
            os.chdir("..")
            print(os.getcwd() + "/db")
            b = gitman.readfile(filepath.defaultLVphy)

            return redirect(url_for('menu'))
        else:
            # Read file path from user
            path = request.form['localpath']
            # Read each file from local path
        # errormesg, mergedfilename = mergedb(rawfilename)
        # errormesg2, datamodelfilename = checkdb(mergedfilename)
        # logfilepath = logfilegen(errormesg, errormesg2, parentdir)
        # logfilegit(gitman, logfilepath)
        # updatefilepath(newfilepath)    
            return render_template('builddatamodel.html', loginstatus = loginstatus)
    elif request.method == 'GET':
        return render_template('builddatamodel.html', loginstatus = loginstatus)


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    global loginstatus
    return render_template('menu.html', loginstatus = loginstatus)

if __name__ == '__main__':
    # The server is run directly
    app.debug = True
    app.run()
# else: (If imported by another module)