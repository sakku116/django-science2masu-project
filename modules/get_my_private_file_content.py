from github import Github
from dotenv import load_dotenv

def getMyPrivateFileContent(repo_name="", file_path="", token=""):
    '''
    get my letter file from my github private repo

    repo_name = "user/repo"
    file_path = "path/to/file.txt"
    token = "github_token"
    '''

    # init
    gh = Github(token)
    repo = gh.get_repo(repo_name)

    contents = repo.get_contents(file_path)

    return contents.decoded_content.decode()