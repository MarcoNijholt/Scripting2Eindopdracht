#!C:\Python34\python.exe
import cgitb
cgitb.enable()
import os
import cgi
import sqlite3
print('Status: 200 OK')
print('Content-type: text/html')
print()
os.environ[ 'HOME' ] = 'G:/User Storage/PycharmProjects/Scripting 2 Eindopdracht/Management/cgi'
import matplotlib
matplotlib.use('Agg')
import pylab as plt


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
    hostnameFileSafe = x['hostname'].replace(".", "_")
    print('<div id="menu'+str(x['id'])+'" class="tab-pane fade"><h3>'+x['hostname']+'</h3>')
    print('<image src="/img/cpu_'+hostnameFileSafe+'.png"> </image>')
    print('<p>')

    queryData = (x['hostname'],)
    c.execute('SELECT * FROM historicalData where hostname = ? order by id desc', queryData)
    cpuData = []
    for x2 in c.fetchall():
        cpuData.append(x2['cpuUssage'])
    plt.figure()
    plt.plot(cpuData)
    plt.ylabel('CPU ussage')
    plt.savefig("img/cpu_"+hostnameFileSafe+".png", transparent=True)

    print('</p>')
    print('</div>')





print("</div></table>")

with open("footer.html", "r") as f:
    print(f.read())

conn.close()