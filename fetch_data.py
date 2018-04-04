"""
Exports Issues from a specified repository to a CSV file
Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import csv
import requests
import random

GITHUB_USER = ''
GITHUB_PASSWORD = ''
REPO = ''  # format is username/repo
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues' % REPO
AUTH = (GITHUB_USER, GITHUB_PASSWORD)
AVG_NUM_OF_TICKETS=10
team = []
team_copy = team.copy()
counter = {}

def write_issues(response):
    "output a list of issues to csv"
    if not r.status_code == 200:
        raise Exception(r.status_code)
    for issue in r.json():
        if issue['state'] == "open" and '/pull/' not in issue['html_url'] and '2018' in issue['created_at'] and len(issue['labels']) == 0:
            if len(team) > 0:
                member = random.choice(team)
                counter[member] = counter[member] + 1 if member in counter else 1
                if counter[member] >= AVG_NUM_OF_TICKETS:
                    team.remove(member)
            else:
                member = random.choice(team_copy)
                counter[member] = counter[member] + 1 if member in counter else 1
            csvout.writerow([issue['number'], issue['state'], issue['title'], issue['html_url'], issue['created_at'], issue['updated_at'], member , ''])


r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))
csvout = csv.writer(open(csvfile, 'w+', newline=''))
csvout.writerow(('id', 'State', 'Title', 'Url', 'Created At', 'Updated At', 'Assignee', 'Note'))
write_issues(r)

#more pages? examine the 'link' header returned
if 'link' in r.headers:
    pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])
    while 'next' in pages:
        r = requests.get(pages['next'], auth=AUTH)
        write_issues(r)
        pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])

print(counter)
print(sum(list(counter.values())))