#!C:\Python34\python.exe
import sqlite3
import cgitb
import json
cgitb.enable()
print('Status: 200 OK')
print('Content-type: text/html')
print()


with open("navbar.html", "r") as f:
    print(f.read())
conn = sqlite3.connect('../networkmonitoring.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

print('<table class="table table-hover">')
print('<tr><th>ID</th><th>timestamp</th><th>host</th><th>os</th><th>diskfree</th><th>disksize</th><th>uptime</th><th>ips</th><th>memfree</th><th>memtotal</th><th>proc count</th><th>cpu ussage</th></tr>')
c.execute('SELECT * FROM historicalData order by id desc limit 1000')



for x in c.fetchall():
    ips = json.loads(x['ips'])
    ipstring = ""
    for ip in ips:
        ipstring += ip + ", "

    ipstring = ipstring[0:-2]
    print('<tr><td>'+str(x['id'])+'</td><td>'+x['timestamp']+'</td><td>'+x['hostname']+'</td><td>'+x['os']+'</td>')
    print('<td>'+str(round(float(x['diskFree'].replace(',','.'))))+'MB</td><td>'+str(round(float(x['diskSize'].replace(',','.'))))+'MB</td>')
    print('<td>'+x['uptime']+'</td><td>'+ipstring+'</td><td>'+str(round(float(x['memFree'].replace(',','.'))))+'MB</td>')
    print('<td>'+str(round(float(x['memTotal'].replace(',','.'))))+'MB</td><td>'+x['proccount']+'</td><td>'+x['cpuUssage']+'%</td></tr>')

conn.close()

print("</table>")

with open("footer.html", "r") as f:
    print(f.read())