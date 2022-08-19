from github import Github

def getGhBlobList(
        github_token = "",
        github_repo = "",
        prefix = "",
    ):
    ''' get list of blob from github repository '''

    try:
        # init github
        if github_token:
            gh = Github(github_token) # use token (optional) to prevent api request limitation
        else:
            gh = Github()
        repo = gh.get_repo(github_repo)

        BASE_RAW_GH_URL = 'https://raw.githubusercontent.com/sakku116/science2masu-static-files/main/'

        # remove trailing slash in the start and the end of prefix string
        if prefix[0] == '/':
            prefix = prefix[1:]
        if prefix[-1] == '/':
            prefix = prefix[:-1]

        # return list of blobs (including dir type but without it children)
        contents = repo.get_contents(prefix)

        result_list = []

        for content in contents:
            file_path = content.path # return only file path without base url
            file_url = BASE_RAW_GH_URL + file_path
            
            # exclude non file type
            if '.' in file_path.split('/')[-1]:
                result_list.append(file_url)


        return result_list

    except:
        return ['error']