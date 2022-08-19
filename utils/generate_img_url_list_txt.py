'''
run this script to update img_url_list.txt file if there is update in the static files repository

edit the 'prefixes' if needed
'''

from pathlib import Path
from github import Github
from dotenv import load_dotenv
import os

prefixes = [
    'static/images',
    'static/images/gallery',
    'static/images/gallery/others'
]

BASE_DIR = str(Path(__file__).parent.parent)

# load .env file from base dir
load_dotenv(f"{BASE_DIR}/.env")

BASE_OUTPUT_DIR = f"{BASE_DIR}/"
BASE_RAW_GH_URL = 'https://raw.githubusercontent.com/sakku116/science2masu-static-files/main/'

# init github
gh = Github(os.environ.get('GITHUB_TOKEN')) # use token (optional) to prevent api request limitation
repo = gh.get_repo("sakku116/science2masu-static-files")

def generateListInTxt(prefix):
    if prefix[0] == '/':
        prefix = prefix[1:]
    if prefix[-1] == '/':
        prefix = prefix[:-1]

    # return list of blobs (including dir type but without it children)
    contents = repo.get_contents(prefix)

    # sync output file path with prefix
    output_file = f'{BASE_OUTPUT_DIR}{prefix}/img_url_list.txt'
    print(f'output_file = {output_file}')

    with open(output_file, 'w') as f:
        for content in contents:
            file_path = content.path # return only path without base_url
            file_url = BASE_RAW_GH_URL+file_path
            
            # exclude non file type
            if '.' in file_path.split('/')[-1]:
                f.write(file_url)
                f.write('\n')

# generate multiple file in defferent directory
for prefix in prefixes:
    generateListInTxt(prefix)