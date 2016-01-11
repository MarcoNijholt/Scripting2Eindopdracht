import sqlite3

conn = sqlite3.connect('networkmonitoring.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS servers
             (id INTEGER PRIMARY KEY, hostname TEXT, port TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS historicalData
             (id INTEGER PRIMARY KEY, timestamp TEXT, hostname TEXT, os TEXT, diskFree TEXT, diskSize TEXT, uptime TEXT, ips TEXT, memFree TEXT, memTotal TEXT, proccount TEXT, cpuUssage TEXT)''')

c.execute('''select * from servers''')
for x in c.fetchall():
    print("ID:", x[0], "HOST:", x[1], "PORT:", x[2])

id = input("What server ID would you like to remove?: \n")
try:
    id = int(id)
except:
    print("invalid choice, try again by rerunning this script")
    conn.close()
    quit()

try:
    insertData = (id,)
    c.execute('''DELETE FROM servers where id = ?''', insertData)
except:
    print("Deleting the server failed, please try again by rerunning this script.")
else:
    print("Removed the server from the database, restart the management.py script for this change to take effect.")

conn.commit()
conn.close()