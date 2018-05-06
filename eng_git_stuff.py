import gitlab

# private token or personal token authentication
gl = gitlab.Gitlab('https://eng-git.canterbury.ac.nz/',
                   private_token='e-bDxiWe5bwz43WnKUyU')
projects = gl.projects.get('seng302-2018/team-700')
commit= projects.commits.get("9f15c832")
print(commit.title)
b=['9f15c832', '50f7db2b', '9951ea73', '0f3751ae', '05dc0acc', '8082cd07']
