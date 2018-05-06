import MySQLdb
from hash_extractor import *
import plot_graph
import networkx as nx
import gitlab

# private token or personal token authentication
gl = gitlab.Gitlab('https://eng-git.canterbury.ac.nz/',
                   private_token='e-bDxiWe5bwz43WnKUyU')
projects = gl.projects.get('seng302-2018/team-700')


GET_EVERYTHING = """
SELECT description AS story_description,
       name        AS story_name,
       fullName,
       date,
       commit_description,
       minutesspent,
       user_id,
       task_id,
       story_id,
       storyPoints
FROM   (SELECT date,
               hourentries.description AS commit_description,
               minutesspent,
               user_id,
               task_id,
               tasks.story_id
        FROM   hourentries
               LEFT JOIN tasks
                      ON tasks.id = hourentries.task_id)AS T
       LEFT JOIN stories
              ON stories.id = T.story_id
       LEFT JOIN users
   	      ON users.id=T.user_id
WHERE  user_id IN ( {} )
       AND date >= "2018-03-26"
       AND T.story_id {} NULL
"""


def find_member(cursor):
    cursor.execute(
        'SELECT id,fullName FROM users WHERE initials IN ("jto59","tke29","och26","ewi32","mjs351","dca87","ato47","jes143")')
    member_map={}
    for row in cursor.fetchall():
        member_map[str(row['id'])]=row['fullName']
    return member_map


def db_connect():
    db = MySQLdb.connect(host="mysql.cosc.canterbury.ac.nz",    # your host, usually localhost
                         user="af-seng401",         # your username
                         passwd="LucianoNimrod4252",  # your password
                         db="agilefant302")        # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    return db, db.cursor(MySQLdb.cursors.DictCursor)


def tag_stats(task_with_out_story=True):
    db, cur = db_connect()
    members = find_member(cur)
    if task_with_out_story:
        cur.execute(GET_EVERYTHING.format(",".join(members.keys()), "IS NOT"))
    else:
        cur.execute(GET_EVERYTHING.format(",".join(members.keys()), "IS"))

    counter = 0
    hash_dict = {'#invalid': 0, '#none': 0}
    invalid_dict = {}
    for row in cur.fetchall():
        counter += 1
        valid, invalid = extract_hash(row['commit_description'])
        if len(valid + invalid) == 0:
            hash_dict['#none'] += 1
            continue
        for good in valid:
            if good == "#commits":
                continue
            if good not in hash_dict.keys():
                hash_dict[good] = 0
            hash_dict[good] += 1
        for bad in invalid:
            hash_dict['#invalid'] += 1
            if bad not in invalid_dict.keys():
                invalid_dict[bad] = 0
            invalid_dict[bad] += 1
    plot_graph.plot_tags(hash_dict, invalid_dict)
    db.close()


def time_stats():
    db, cur = db_connect()
    members = find_member(cur)
    cur.execute(GET_EVERYTHING.format(",".join(members.keys()), "IS NOT"))
    name = []
    mapped_name=[]
    time_spent = []
    commit_length=[]
    for row in cur.fetchall():
        result = extract_commit(row["commit_description"])
        if result:
            total_length=0
            result=result.split(",")
            for i in result:
                i=i.strip()
                try:
                    commit= projects.commits.get(i)
                    total_length+=len(commit.message)
                except Exception as e:
                    print(i)
                    commit= projects.commits.get("9951ea7e")
                    total_length+=len(commit.message)
            commit_length.append(total_length)

            name.append(row["fullName"])
            time_spent.append(int(row["minutesspent"]))
    plot_graph.plot_scatter_with_line(name, time_spent)
    plot_graph.plot_scatter(time_spent,commit_length,name,"Commit Length Analysis","Gitlab commit length","Time spent")
    db.close()


def bus_factor():
    """for each story find hours worked for each member"""
    db, cur = db_connect()
    members = find_member(cur)
    cur.execute(GET_EVERYTHING.format(",".join(members.keys()), "IS NOT"))
    story_dict = {}
    for row in cur.fetchall():
        story_name = row["story_name"].split('.')[0]
        if story_name not in story_dict.keys():
            story_dict[story_name] = {}
        if row["fullName"] not in story_dict[story_name].keys():
            story_dict[story_name][row["fullName"]] = 0
        story_dict[story_name][row["fullName"]] += row["minutesspent"]
    plot_graph.plot_stacked_bar(story_dict, sorted(list(members.values())))
    db.close()


def pp_graph():
    G = nx.Graph()
    db, cur = db_connect()
    members = find_member(cur)
    cur.execute(GET_EVERYTHING.format(",".join(members.keys()), "IS NOT"))
    for row in cur.fetchall():
        pair = find_pairs(row["commit_description"])
        if pair:
            if G.has_edge(pair[0], pair[1]):
                G[pair[0]][pair[1]]['weight'] += 1
            else:
                # new edge. add with weight=1
                G.add_edge(pair[0], pair[1], weight=1)
    plot_graph.draw_network(G)

if __name__ == '__main__':
    bus_factor()
    tag_stats()
    time_stats()

    pp_graph()
