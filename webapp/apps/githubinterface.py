from github import Github

global g
def githublogin(username, githubpat):
    g = Github(githubpat)
    try:
        repo = g.get_repo("kthfspe/SA")
        return True
    except:
        return False
        

