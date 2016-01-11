#!C:\Python34\python.exe
import cgitb
cgitb.enable()
import os
import sqlite3
import json

# Send out headers
print('Status: 200 OK')
print('Content-type: text/html')
print()

# needed so matplotlib can run in CGI mode
os.environ[ 'HOME' ] = 'G:/User Storage/PycharmProjects/Scripting 2 Eindopdracht/Management/cgi'
import matplotlib
# set non GUI mode
matplotlib.use('Agg')
import pylab as plt

# import the navbar html file for static website data
with open("navbar.html", "r") as f:
    print(f.read())

# open DB connection for server and historical data
conn = sqlite3.connect('../networkmonitoring.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute('SELECT * FROM servers')
servers = c.fetchall()
print("<h1>Servers</h1>")
print('<ul class="nav nav-tabs"><li class="active"><a data-toggle="tab" href="#home">Home</a></li>')
# create a list of servers for the tabbed element
for x in servers:
    print('<li><a data-toggle="tab" href="#menu'+str(x['id'])+'">'+x['hostname']+'</a></li>')


print('</ul><div class="tab-content"><div id="home" class="tab-pane fade in active">')
print('<h3>HOME</h3><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p></div>')

# occupy the tabbed elements with data
for x in servers:
    hostnameFileSafe = x['hostname'].replace(".", "_")
    print('<div id="menu'+str(x['id'])+'" class="tab-pane fade"><h3>'+x['hostname']+'</h3>')
    print('<div class="row">')
    print('<div class="col-lg-12">')
    queryData = (x['hostname'],)
    c.execute('SELECT * FROM historicalData where hostname = ? order by id desc limit 1', queryData)
    latestPoll = c.fetchone()
    ips = json.loads(latestPoll['ips'])
    ipstring = ""
    for ip in ips:
        ipstring += ip + ", "

    ipstring = ipstring[0:-2]
    # calculate the usage % and round them to 2 decimals and converting them to strings
    diskUssage = str(round(100 - ((float(latestPoll['diskFree'].replace(",",".")) / float(latestPoll['diskSize'].replace(",","."))) * 100), 2))
    memUssage = str(round(100 - ((float(latestPoll['memFree'].replace(",",".")) / float(latestPoll['memTotal'].replace(",","."))) * 100), 2))

    print('<table class="table table-hover table-striped">')
    print('<tr><td>Operating System</td><td>'+latestPoll['os']+'</td></tr>')
    print('<tr><td>Uptime</td><td>'+latestPoll['uptime']+'</td></tr>')
    print('<tr><td>Available IPv4 Addresses</td><td>'+ipstring+'</td></tr>')
    print('<tr><td>Latest Poll</td><td>'+latestPoll['timestamp']+'</td></tr>')
    print('<tr><td>Latest CPU Usage</td><td>'+latestPoll['cpuUssage']+'%</td></tr>')
    print('<tr><td>Latest Proc Count</td><td>'+latestPoll['proccount']+' Processes</td></tr>')
    print('<tr><td>Latest Disk Usage</td><td>'+diskUssage+'%</td></tr>')
    print('<tr><td>Latest Memory Usage</td><td>'+memUssage+'%</td></tr>')
    print('</table>')
    print('</div>')

    print('<div class="col-lg-6" style="text-align:center;"><h4>CPU Usage</h4><image width="100%" src="/img/cpu_'+hostnameFileSafe+'.png"> </image></div>')
    print('<div class="col-lg-6" style="text-align:center;"><h4>Disk Usage</h4><image width="100%" src="/img/disk_'+hostnameFileSafe+'.png"> </image></div>')
    print('<div class="col-lg-6" style="text-align:center;"><h4>Memory Usage</h4><image width="100%" src="/img/mem_'+hostnameFileSafe+'.png"> </image></div>')
    print('<div class="col-lg-6" style="text-align:center;"><h4>Process Count</h4><image width="100%" src="/img/procc_'+hostnameFileSafe+'.png"> </image></div>')


    queryData = (x['hostname'],)
    c.execute('SELECT * FROM historicalData where hostname = ? order by id desc', queryData)
    # declare the lists for the plot data
    cpuData = []
    memData = []
    diskData = []
    proccData = []
    for x2 in c.fetchall():
        # populate lists
        cpuData.append(x2['cpuUssage'])
        proccData.append(x2['proccount'])
        diskUssage = 100 - ((float(x2['diskFree'].replace(",",".")) / float(x2['diskSize'].replace(",","."))) * 100)
        diskData.append(round(diskUssage))
        memUssage = 100 - ((float(x2['memFree'].replace(",",".")) / float(x2['memTotal'].replace(",","."))) * 100)
        #print(memUssage)
        memData.append(round(memUssage))

    # Plot the figures with the data generated in the previous lists
    plt.figure()
    plt.plot(cpuData)
    plt.ylabel('CPU ussage %')
    plt.xlabel("Polling number")
    plt.savefig("img/cpu_"+hostnameFileSafe+".png", transparent=True)

    plt.figure()
    plt.plot(diskData)
    plt.ylabel('Disk ussage %')
    plt.xlabel("Polling number")
    plt.savefig("img/disk_"+hostnameFileSafe+".png", transparent=True)

    plt.figure()
    plt.plot(memData)
    plt.ylabel('Memory ussage %')
    plt.xlabel("Polling number")
    plt.savefig("img/mem_"+hostnameFileSafe+".png", transparent=True)

    plt.figure()
    plt.plot(proccData)
    plt.ylabel('Process Count')
    plt.xlabel("Polling number")
    plt.savefig("img/procc_"+hostnameFileSafe+".png", transparent=True)

    print('</div>')
    print('</div>')

print("</div></table>")

with open("footer.html", "r") as f:
    print(f.read())

conn.close()