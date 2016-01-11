#!C:\Python34\python.exe
import sqlite3
import cgitb
import csv
import io
cgitb.enable()

# print http headers
print('Status: 200 OK')
print('Content-type: text/html')
print()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# import static html navbar
with open("navbar.html", "r") as f:
    print(f.read())

# setup db
conn = sqlite3.connect('../networkmonitoring.db')
c = conn.cursor()

# write csv to dummy IO so it can be displayed on page.
serverCSVOutput = io.StringIO()
# get keys for header
c.execute('PRAGMA table_info(servers)')
serverListKeys = []
for key in c.fetchall():
    serverListKeys.append(key[1])
c.execute('SELECT * FROM servers')
serverList = c.fetchall()
writer = csv.writer(serverCSVOutput)
writer.writerow(serverListKeys)
writer.writerows(serverList)


latestCountersCSVOutput = io.StringIO()
c.execute('PRAGMA table_info(historicalData)')
latestCountersListKeys = []
for key in c.fetchall():
    latestCountersListKeys.append(key[1])
writer = csv.writer(latestCountersCSVOutput)
writer.writerow(latestCountersListKeys)

c.execute('SELECT hostname FROM servers')
serverList = c.fetchall()
for server in serverList:
    whereData = (server[0],)
    c.execute('SELECT * FROM historicalData where hostname = ? limit 1', whereData)
    latestCountersList = c.fetchone()
    writer.writerow(latestCountersList)


countersCSVOutput = io.StringIO()
c.execute('PRAGMA table_info(historicalData)')
countersListKeys = []
for key in c.fetchall():
    countersListKeys.append(key[1])
c.execute('SELECT * FROM historicalData limit 10000')
countersList = c.fetchall()
writer = csv.writer(countersCSVOutput)
writer.writerow(countersListKeys)
writer.writerows(countersList)





print('<h2>Server Information as CSV <h2><button id="downloadServer" style="margin-bottom:10px;margin-top:0px;" class="btn btn-success">Download CSV</button>')
print('<pre style="max-height:200px;" id="downloadServerContent">')
print(serverCSVOutput.getvalue())
print('</pre>')
print('<h2->Latest Counters for each servers as CSV <h2><button id="downloadLatest" style="margin-bottom:10px;margin-top:0px;" class="btn btn-success">Download CSV</button>')
print('<pre style="max-height:250px;" id="downloadLatestContent">')
print(latestCountersCSVOutput.getvalue())
print('</pre>')
print('<h2->Agent Counters CSV<h2><button id="downloadTotal" style="margin-bottom:10px;margin-top:0px;" class="btn btn-success">Download CSV</button>')
print('<pre style="max-height:350px;" id="downloadTotalContent">')
print(countersCSVOutput.getvalue())
print('</pre>')
with open("footer.html", "r") as f:
    print(f.read())