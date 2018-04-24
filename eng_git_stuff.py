import requests
import json
url = "https://eng-git.canterbury.ac.nz/api/v4/projects/3347/repository/commits"

headers = {
    'private-token': "e-bDxiWe5bwz43WnKUyU",
    'cache-control': "no-cache",
    'postman-token': "d6f9093f-e68d-4cd8-faf8-644823fb2751"
    }

response = requests.request("GET", url, headers=headers)
commits=response.json()
for commit in commits:
    # commit=commit.encode('utf-8')
    print(commit['committed_date'].encode('utf-8'))
