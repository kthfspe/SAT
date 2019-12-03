from app import app
from flask_github import GitHub

app.config['GITHUB_CLIENT_ID'] = '14752ee16c6d1630fe01XXX'
app.config['GITHUB_CLIENT_SECRET'] = '73a4097d241175d0bfdff2c31bb49efa229ea8da'

github = GitHub(app)

if __name__ == "__main__":
    app.run()