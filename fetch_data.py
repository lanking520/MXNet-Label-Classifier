"""
Exports Issues from a specified repository to a CSV file
Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import requests
import json

GITHUB_USER = ''
GITHUB_PASSWORD = ''
REPO = ''  # format is username/repo
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues' % REPO
AUTH = (GITHUB_USER, GITHUB_PASSWORD)

def get_issue_json():

    long_live_array = []
    r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
    long_live_array.append(r.json())

    #more pages? examine the 'link' header returned
    if 'link' in r.headers:
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
        while 'next' in pages:
            r = requests.get(pages['next'], auth=AUTH)
            long_live_array.append(r.json())
            pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
    f = open('data.json', 'w')

    f.close()

get_issue_json()