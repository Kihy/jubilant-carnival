import gitlab

# private token or personal token authentication
gl = gitlab.Gitlab('https://eng-git.canterbury.ac.nz/',
                   private_token='e-bDxiWe5bwz43WnKUyU')
projects = gl.projects.get('seng302-2018/team-700')
for commit in projects.commits.list(all=True, since='2018-03-26'):
    print(commit.title)
