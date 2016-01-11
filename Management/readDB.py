import sqlite3
conn = sqlite3.connect('networkmonitoring.db')
c = conn.cursor()

c.execute('SELECT * FROM servers')
for x in c.fetchall():
    print(x)

conn.commit()
conn.close()