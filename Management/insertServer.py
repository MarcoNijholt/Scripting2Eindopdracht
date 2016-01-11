import sqlite3

conn = sqlite3.connect('networkmonitoring.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS servers
             (id INTEGER PRIMARY KEY, hostname TEXT, port TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS historicalData
             (id INTEGER PRIMARY KEY, timestamp TEXT, hostname TEXT, os TEXT, diskFree TEXT, diskSize TEXT, uptime TEXT, ips TEXT, memFree TEXT, memTotal TEXT, proccount TEXT, cpuUssage TEXT)''')

serverHost = input("What is the server hostname? so for example: 192.168.1.1: \n")
serverPort = input("On what port does the agent run? Default is 8888: \n")

try:
    insertData = (serverHost, serverPort)
    c.execute('''INSERT INTO servers
                 (hostname,port) VALUES (?,?)''', insertData)
except:
    print("Failed to insert the server into the DB, please try again")
else:
    print("Inserted the server into the database, please restart the management script for this change to take effect.")

conn.commit()
conn.close()