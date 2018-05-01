import MySQLdb
from hash_extractor import *
import plot_graph

GET_EVERYTHING="""
SELECT description AS story_description,
       name        AS story_name,
       date,
       commit_description,
       minutesspent,
       user_id,
       task_id,
       story_id
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
WHERE  user_id IN ( 540, 548, 555, 560,
                    578, 590, 605, 618 )
       AND date >= "2018-03-26"
       AND T.story_id IS NOT NULL
"""
def find_member(cursor):
    cursor.execute('SELECT id,fullName FROM users WHERE initials IN ("jto59","tke29","och26","ewi32","mjs351","dca87","ato47","jes143")')
    ids=[]
    for row in cursor.fetchall():
        ids.append(str(int(row[0])))
    return ",".join(ids)

def db_connect():
    db = MySQLdb.connect(host="mysql.cosc.canterbury.ac.nz",    # your host, usually localhost
                     user="af-seng401",         # your username
                     passwd="LucianoNimrod4252",  # your password
                     db="agilefant302")        # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    return db, db.cursor()

def tag_stats():
    db,cur=db_connect()
    members=find_member(cur)
    cur.execute(
            'SELECT description FROM hourentries WHERE user_id IN ({}) AND date >= \"2018-03-26\"'.format(members))

    counter=0
    hash_dict={'#invalid':0, '#none':0}
    invalid_dict={}
    for row in cur.fetchall():
        counter+=1
        valid, invalid=extract_hash(row[0])
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
    plot_pretty_graphs(hash_dict,invalid_dict)
    db.close()

def plot_pretty_graphs(hash_dict,invalid_dict):
    #plots summarized hashes
    labels=[]
    values=[]
    explode=[]
    for label,freq in hash_dict.items():
        labels.append(label)
        values.append(freq)
        if label=='#invalid':
            explode.append(0.05)
        else:
            explode.append(0)
    plot_graph.plot_pie(labels,values,explode)

    #plots invalid hashes
    plot_graph.plot_pie(list(invalid_dict.keys()),list(invalid_dict.values()),startangle=0)

def time_stats():
    db,cur=db_connect()
    members=find_member(cur)
    cur.execute(
            'SELECT description,minutesSpent,user_id FROM hourentries WHERE user_id IN ({}) AND date >= \"2018-03-26\" AND story_id != NULL'.format(members))
    print('SELECT description,minutesSpent,user_id FROM hourentries WHERE user_id IN ({}) AND date >= \"2018-03-26\" AND story_id != NULL'.format(members))
    user_id=[]
    time_spent=[]
    for row in cur.fetchall():
        valid,invalid=extract_hash(row[0],"commits")
        if len(valid+invalid)!=0:
            user_id.append(row[2])
            time_spent.append(int(row[1]))
    plot_graph.plot_scatter(user_id,time_spent)
    db.close()

def bus_factor():
    db,cur=db_connect()
    members=find_member(cur)
    cur.execute(
            'SELECT description,minutesSpent,user_id,story_id,backlog_id,task_id FROM hourentries WHERE user_id IN ({}) AND date >= \"2018-03-26\"'.format(members))
    for row in cur.fetchall():
        print(row)
    db.close()
time_stats()
