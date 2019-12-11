from github import Github

g = ""
def githublogin(username, githubpat):
    global g
    g = Github(githubpat)
    try:
        repo = g.get_repo("kthfspe/SA")
        return True
    except:
        return False

def fetchlatestcommit():
    pass
        

