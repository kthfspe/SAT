import sys
import os
sys.path.insert(0,os.getcwd()+"/scripts")
from flask import Flask, url_for, render_template, request, redirect
from gitmanager import GitManager
from datamanager import DataManager
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
    if request.method == 'POST':
        option = request.form['options']
        if option == "github":
            # Read each file from github
            raw_functional = gitman.readfile(filepath.defaultLVfun)
            raw_functional.append(gitman.readfile(filepath.defaultHVfun))
            raw_functional.append(gitman.readfile(filepath.defaultDVfun))
            raw_physical = gitman.readfile(filepath.defaultLVphy)
            raw_physical.append(gitman.readfile(filepath.defaultHVphy))
            raw_physical.append(gitman.readfile(filepath.defaultDVphy))       
        else:
            # Read file path from user
            path = request.form['localpath']
            raw_functional = localreadfile(filepath.localLVfun)
            raw_functional.append(localreadfile(filepath.localHVfun))
            raw_functional.append(localreadfile(filepath.localDVfun))
            raw_physical = localreadfile(filepath.localLVphy)
            raw_physical.append(localreadfile(filepath.localHVphy))
            raw_physical.append(localreadfile(filepath.localDVphy))            
        return redirect(url_for('menu')) 
        # errormesg, mergedfilename = mergedb(rawfilename)
        # errormesg2, datamodelfilename = checkdb(mergedfilename)
        # logfilepath = logfilegen(errormesg, errormesg2, parentdir)
        # logfilegit(gitman, logfilepath)
        # updatefilepath(newfilepath)    
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