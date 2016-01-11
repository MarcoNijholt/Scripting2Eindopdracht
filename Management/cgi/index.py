#!C:\Python34\python.exe
import sqlite3
import cgitb
cgitb.enable()
print('Status: 200 OK')
print('Content-type: text/html')
print()


with open("navbar.html", "r") as f:
    print(f.read())
conn = sqlite3.connect('../networkmonitoring.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute('SELECT * FROM servers')
servers = c.fetchall()
print("<h1>Servers</h1>")
print('<ul class="nav nav-tabs"><li class="active"><a data-toggle="tab" href="#home">Home</a></li>')
for x in servers:
    print('<li><a data-toggle="tab" href="#menu'+str(x['id'])+'">'+x['hostname']+'</a></li>')


print('</ul><div class="tab-content"><div id="home" class="tab-pane fade in active">')
print('<h3>HOME</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p></div>')


for x in servers:
    # print(x)
    print('<div id="menu'+str(x['id'])+'" class="tab-pane fade"><h3>'+x['hostname']+'</h3>')
    print('<p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>')
    print('</div>')







# print('<table class="table table-hover">')
# print('<tr><th>ID</th><th>timestamp</th><th>host</th><th>os</th><th>diskfree</th><th>disksize</th><th>uptime</th><th>ips</th><th>memfree</th><th>memtotal</th><th>proc count</th><th>cpu ussage</th></tr>')
# c.execute('SELECT * FROM historicalData order by id desc')
# for x in c.fetchall():
#     print('<tr><td>'+str(x['id'])+'</td><td>'+x['timestamp']+'</td><td>'+x['hostname']+'</td><td>'+x['os']+'</td>')
#     print('<td>'+str(round(float(x['diskFree'].replace(',','.'))))+'MB</td><td>'+str(round(float(x['diskSize'].replace(',','.'))))+'MB</td>')
#     print('<td>'+x['uptime']+'</td><td>ips</td><td>'+str(round(float(x['memFree'].replace(',','.'))))+'MB</td>')
#     print('<td>'+str(round(float(x['memTotal'].replace(',','.'))))+'MB</td><td>'+x['proccount']+'</td><td>'+x['cpuUssage']+'%</td></tr>')


print("</div></table>")

with open("footer.html", "r") as f:
    print(f.read())

conn.close()