import sys
import os
sys.path.insert(0,os.getcwd()+"/scripts")
from flask import Flask, url_for, render_template, request, redirect
from gitmanager import GitManager
from datamanager import DataManager
from dbmanager import DBManager
from localfile import readdrawiofile
import yaml
import searchname
import applist

# from scripts.usermanager import UserManager
import satconfig

# Create Flask App object
app = Flask(__name__)

# Create git object to interface to Github
gitman = GitManager()
dataman = DataManager()
loginstatus = False
error = []

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global loginstatus
    # Read config file
    with open(satconfig.config["configyamlfilename"], 'r') as file:
        documents = yaml.load(file)
    error = None
    if request.method == 'POST':
        if gitman.gitlogin(request.form['password']) == True:
            loginstatus = True
            return redirect(url_for('menu'))
        else:
            error = "Access Denied. Check your Personal Access Token and your access to repo kthfspe/SA"
            return render_template('login.html', error = error, loginstatus = loginstatus)
    elif request.method == 'GET':
        loginstatus = False
        return render_template('login.html', error=error, loginstatus = False)


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    global loginstatus, error
    raw_functional = []
    raw_physical = []
    if request.method == 'GET':
        # Read each file from github
        if satconfig.config["debug"]== False:
            raw_functional1 = gitman.readfile(satconfig.config["defaultLVfun"])
            raw_functional2 = gitman.readfile(satconfig.config["defaultHVfun"])
            raw_functional3 = gitman.readfile(satconfig.config["defaultDVfun"])
            raw_functional = raw_functional1 + raw_functional2 + raw_functional3
            raw_physical1 = gitman.readfile(satconfig.config["defaultLVphy"])
            raw_physical2 = gitman.readfile(satconfig.config["defaultHVphy"])
            raw_physical3 = gitman.readfile(satconfig.config["defaultDVphy"])
            raw_physical = raw_physical1 + raw_physical2 + raw_physical3       
        else:
            raw_functional1 = gitman.readfile(satconfig.config["exampleLVfun"])
            raw_functional2 = gitman.readfile(satconfig.config["exampleHVfun"])
            raw_functional3 = gitman.readfile(satconfig.config["exampleDVfun"])
            raw_functional = raw_functional1 + raw_functional2 + raw_functional3
            raw_physical1 = gitman.readfile(satconfig.config["exampleLVphy"])
            raw_physical2 = gitman.readfile(satconfig.config["exampleHVphy"])
            raw_physical3 = gitman.readfile(satconfig.config["exampleDVphy"])
            raw_physical = raw_physical1 + raw_physical2 + raw_physical3       

        # Build data model using the raw data
        buildmodelerror, buildmodelstatus= dataman.buildmodel(raw_functional, raw_physical)
        if  buildmodelstatus != 0:
            return render_template('error.html', loginstatus = loginstatus, error = buildmodelerror)
        elif buildmodelerror != []:
            return render_template('menu.html', loginstatus = loginstatus, appdata=applist.appdata)
            # Menu with warning
        else:
            # Menu without any warning
            return render_template('menu.html')

        # Save errors, warnings to log file

        
    elif request.method == 'POST':
        print("Menu Post")
        return render_template('menu.html', loginstatus = loginstatus)


@app.route('/output', methods=['GET', 'POST'])
def output():
    global loginstatus,error, warning

    return render_template('output.html', loginstatus = loginstatus)

@app.route('/error', methods=['GET', 'POST'])
def error():
    global loginstatus,error

    return render_template('error.html', loginstatus = loginstatus, error = error)




@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global loginstatus
    if request.method == "GET":
        if request.args.get("submitbutton") == "Apply & Rebuild Model":
            for item in satconfig.config["settingspagefields"]:
                satconfig.config[item] = request.args.get(item)
            if request.args.get("debug"):
                satconfig.config["debug"] = True
            else:
                satconfig.config["debug"] = False
            # Write this configuration to file
            if os.path.exists(satconfig.config["configyamlfilename"]):
                os.remove(satconfig.config["configyamlfilename"])
            with open(satconfig.config["configyamlfilename"], 'w') as file:
                documents = yaml.dump(satconfig.config, file)
            return redirect(url_for('menu'))
    return render_template('settings.html',loginstatus=loginstatus, config=satconfig.config)

if __name__ == '__main__':
    # The server is run directly
    if os.path.exists(satconfig.config["configyamlfilename"]):
        os.remove(satconfig.config["configyamlfilename"])
    with open(satconfig.config["configyamlfilename"], 'w') as file:
        documents = yaml.dump(satconfig.config, file)  
    app.debug = True
    app.run()
# else: (If imported by another module)