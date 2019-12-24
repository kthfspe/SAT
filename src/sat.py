import sys
import os
from flask import Flask, url_for, render_template, request, redirect
from scripts.gitmanager import GitManager
from scripts.datamanager import DataManager
# from scripts.usermanager import UserManager
from scripts import filepath

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
    if request.method == 'POST':
        option = request.form['options']
        if option == "github":
            # Read each file from github
            # status, rawfilename =loaddb(functionallist, physicallist, parentdir)

            raw_functional = gitman.readfile(filepath.defaultLVfun)
            raw_functional.append(gitman.readfile(filepath.defaultHVfun))
            raw_functional.append(gitman.readfile(filepath.defaultDVfun))
            raw_physical = gitman.readfile(filepath.defaultLVphy)
            raw_physical.append(gitman.readfile(filepath.defaultHVphy))
            raw_physical.append(gitman.readfile(filepath.defaultDVphy))
            os.chdir("..")
            parentdir = os.getcwd()+"db"
            os.chdir("src")
            dataman.loaddb(raw_functional, raw_physical, os.getcwd()+"/db")
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