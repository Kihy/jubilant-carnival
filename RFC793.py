import MySQLdb
from hash_extractor import *
import plot_graph

GET_EVERYTHING="""
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
    cursor.execute('SELECT id,fullName FROM users WHERE initials IN ("jto59","tke29","och26","ewi32","mjs351","dca87","ato47","jes143")')
    ids=[]
    fullNames=[]
    for row in cursor.fetchall():
        ids.append(str(int(row['id'])))
        fullNames.append(row['fullName'])
    return ",".join(ids),fullNames

def db_connect():
    db = MySQLdb.connect(host="mysql.cosc.canterbury.ac.nz",    # your host, usually localhost
                     user="af-seng401",         # your username
                     passwd="LucianoNimrod4252",  # your password
                     db="agilefant302")        # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    return db, db.cursor(MySQLdb.cursors.DictCursor)

def tag_stats(task_with_out_story=True):
    db,cur=db_connect()
    members,_=find_member(cur)
    if task_with_out_story:
        cur.execute(GET_EVERYTHING.format(members,"IS NOT"))
    else:
        cur.execute(GET_EVERYTHING.format(members,"IS"))

    counter=0
    hash_dict={'#invalid':0, '#none':0}
    invalid_dict={}
    for row in cur.fetchall():
        counter+=1
        valid, invalid=extract_hash(row['commit_description'])
        if len(valid+invalid)==0:
            hash_dict['#none']+=1
            continue
        for good in valid:
            if good=="#commits":
                continue
            if good not in hash_dict.keys():
                hash_dict[good]=0
            hash_dict[good]+=1
        for bad in invalid:
            hash_dict['#invalid']+=1
            if bad not in invalid_dict.keys():
                invalid_dict[bad]=0
            invalid_dict[bad]+=1
    plot_graph.plot_tags(hash_dict,invalid_dict)
    db.close()



def time_stats():
    db,cur=db_connect()
    members,_=find_member(cur)
    cur.execute(GET_EVERYTHING.format(members,"IS NOT"))
    name=[]
    time_spent=[]
    for row in cur.fetchall():
        valid,invalid=extract_hash(row["commit_description"],"commits")
        if len(valid+invalid)!=0:
            name.append(row["fullName"])
            time_spent.append(int(row["minutesspent"]))
    plot_graph.plot_scatter(name,time_spent)
    db.close()

def bus_factor():
    """for each story find hours worked for each member"""
    db,cur=db_connect()
    members,fullNames=find_member(cur)
    cur.execute(GET_EVERYTHING.format(members,"IS NOT"))
    story_dict={}
    for row in cur.fetchall():
        story_name=row["story_name"].split('.')[0]
        if story_name not in story_dict.keys():
            story_dict[story_name]={}
        if row["fullName"] not in story_dict[story_name].keys():
            story_dict[story_name][row["fullName"]]=0
        story_dict[story_name][row["fullName"]]+=row["minutesspent"]
    plot_graph.plot_stacked_bar(story_dict,fullNames)
    db.close()

def pp_graph():
    db,cur=db_connect()
    members,_=find_member(cur)
    cur.execute(GET_EVERYTHING.format(members,"IS NOT"))
    for row in cur.fetchall():
        pair= find_pairs(row["commit_description"])
        if pair:
            print(pair)

pp_graph()
