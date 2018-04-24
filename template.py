import MySQLdb

db = MySQLdb.connect(host="mysql.cosc.canterbury.ac.nz",    # your host, usually localhost
                     user="af-seng401",         # your username
                     passwd="LucianoNimrod4252",  # your password
                     db="agilefant302")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# find team members
cur.execute(
    'SELECT id,fullName FROM users WHERE initials IN ("jto59","tke29","och26","ewi32","mjs351","dca87","ato47","jes143")')

#cur.execute("SELECT * FROM hourentries WHERE user_id IN('')")
member_ids=[]
# print all the first cell of all the rows
for row in cur.fetchall():
    member_ids.append(str(int(row[0])))

stuff=",".join(member_ids)

cur.execute(
    'SELECT description,minutesSpent FROM hourentries WHERE user_id IN ({}) AND date >= \"2018-03-26\"'.format(stuff))
for row in cur.fetchall():
    print(row)
db.close()
