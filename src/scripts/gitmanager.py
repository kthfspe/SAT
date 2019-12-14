from github import Github      

class GitManager:
    def __init__(self):
        pass
    
    def gitlogin(self, pat):
        self.gitobject = Github(pat)
        try:
            repo = self.gitobject.get_repo("kthfspe/SA")
            return True
        except:
            print("Access Denied. Check your Personal Access Token and your access to repo kthfspe/SA")
            return False