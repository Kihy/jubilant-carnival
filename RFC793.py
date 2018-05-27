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
       AND date <= "2018-05-24"
       AND T.story_id {} NULL
"""
anon_dict={540:"EXO",
548:"BTS",
555:"BLACKPINK",
560:"f(x)",
578:"GOT7",
590:"Super Junior",
605:"BIGBANG",
618:"SHINee"}

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
    hash_dict = {'invalid': 0, 'none': 0}
    invalid_dict = {}
    for row in cur.fetchall():
        counter += 1
        valid, invalid = extract_hash(row['commit_description'])
        if len(valid + invalid) == 0:
            hash_dict['none'] += 1
            continue
        for good in valid:
            if good == "commits":
                continue
            if good not in hash_dict.keys():
                hash_dict[good] = 0
            hash_dict[good] += 1
        for bad in invalid:
            hash_dict['invalid'] += 1
            if bad not in invalid_dict.keys():
                invalid_dict[bad] = 0
            invalid_dict[bad] += 1
    # plot_graph.plot_tags(hash_dict, invalid_dict)
    f=open("tag_stats.csv","w")
    f.write(",".join(hash_dict.keys()))
    f.write("\n")
    f.write(",".join(str(x) for x in hash_dict.values()))
    f.write("\n")
    f.write(",".join(invalid_dict.keys()))
    f.write("\n")
    f.write(",".join(str(x) for x in invalid_dict.values()))
    f.close()

    db.close()


def time_stats():
    db, cur = db_connect()
    members = find_member(cur)
    cur.execute(GET_EVERYTHING.format(",".join(members.keys()), "IS NOT"))
    name = []
    time_dict={}
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

            name.append(anon_dict[row["user_id"]])
            if anon_dict[row["user_id"]] not in time_dict.keys():
                time_dict[anon_dict[row["user_id"]]]=[]
            # print(float(row["minutesspent"])/len(result))
            time_spent.append(float(row["minutesspent"])/len(result))
            time_dict[anon_dict[row["user_id"]]].append(float(row["minutesspent"])/len(result))
    # plot_graph.plot_scatter_with_line(name, time_spent)
    f=open("time_stats.csv","w")
    for i in time_dict.keys():
        f.write("{},{}\n".format(i,",".join(str(x) for x in time_dict[i])))
    f.close()
    # plot_graph.plot_scatter(time_spent,commit_length,name,"Commit Length Analysis","Gitlab commit length","Time spent")
    db.close()


def bus_factor():
    """for each story find hours worked for each member"""
    db, cur = db_connect()
    members = find_member(cur)
    cur.execute(GET_EVERYTHING.format(",".join(members.keys()), "IS NOT"))
    story_dict = {}
    for row in cur.fetchall():
        story_name = str(row["story_id"])
        if story_name not in story_dict.keys():
            story_dict[story_name] = {}
        if row["user_id"] not in story_dict[story_name].keys():
            story_dict[story_name][row["user_id"]] = 0
        story_dict[story_name][row["user_id"]] += row["minutesspent"]

    # plot_graph.plot_stacked_bar(story_dict, sorted(list(members.keys())))
    print(story_dict)
    fullNames=members.keys()
    story_names = sorted(list(story_dict.keys()))
    fullNames=list(map(int,fullNames))
    member_participation = [[0 for x in range(len(story_names))] for x in range(
        len(fullNames))]  # each row is a member, column is a story
    for i in range(len(story_names)):
        for j in range(len(fullNames)):
            try:
                member_participation[j][i] = story_dict[story_names[i]][fullNames[j]]
            except:
                continue
    f=open("bus_factor.csv","w")
    for i in member_participation:
        f.write(",".join(str(j) for j in i))
        f.write("\n")
    # f.write(",".join(str(x) for x in story_dict.values()))
    f.close()


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
                G[pair[0]][pair[1]]['frequency'] += 1
            else:
                # new edge. add with weight=1
                G.add_edge(pair[0], pair[1], frequency=1)
    plot_graph.draw_network(G)
    print(G.nodes)

if __name__ == '__main__':
    # bus_factor()
    # tag_stats()
    # time_stats()
    #
    pp_graph()
