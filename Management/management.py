import socket
import json
import sqlite3
import datetime
import time
import logging
logging.basicConfig(filename='management.log',level=logging.DEBUG)

conn = sqlite3.connect('networkmonitoring.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS servers
             (id INTEGER PRIMARY KEY, hostname TEXT, port TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS historicalData
             (id INTEGER PRIMARY KEY, timestamp TEXT, hostname TEXT, os TEXT, diskFree TEXT, diskSize TEXT, uptime TEXT, ips TEXT, memFree TEXT, memTotal TEXT, proccount TEXT, cpuUssage TEXT)''')

serverList = []
c.execute('SELECT * FROM servers')
for x in c.fetchall():
    serverList.append({"hostname": x['hostname'], "port": int(x["port"])})


def getCounters(hostname, port, request):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = (hostname, port)
    try:
        sock.connect(server_address)
    except:
        logging.warning(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " Could not connect to agent: " + server_address[0]+":"+str(server_address[1]))
        return {"success": False, "response": "Could not connect to agent"}

    try:
        # Send data
        message = '{"request": "' + request + '", "token": "theoneandonlytoken"}'
        message = message.encode("utf-8")
        sock.sendall(message)
        response = ""
        while "\n" not in response:
            data = sock.recv(128).decode("utf-8")
            response += data
            # print("Received: " + data)
        response = response.replace("\n", "")
    finally:
        sock.close()

    try:
        countersResponse = json.loads(response)
    except:
        countersResponse = {"success": False, "response": "Could not parse server response, unable to get counters"}
        logging.warning(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " Could not parse server response, unable to get counters")

    # print(countersResponse)
    if countersResponse['success']:
        timeStamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        ips = json.dumps(countersResponse['response']['ips'])
        newSubInfo = (timeStamp, hostname, countersResponse['response']['os'], countersResponse['response']['disk']['free'],
                      countersResponse['response']['disk']['size'], countersResponse['response']['uptime'], ips,
                      countersResponse['response']['memory']['freeMem'], countersResponse['response']['memory']['totalMem'],
                      countersResponse['response']['proccount'], countersResponse['response']['cpuUssage'])
        try:
            c.execute("INSERT INTO historicalData (timestamp, hostname, os, diskFree, diskSize, uptime, ips, memFree, memTotal, proccount, cpuUssage) VALUES (?,?,?,?,?,?,?,?,?,?,?)", newSubInfo)
            conn.commit()
            return {"success": True, "response": "Data has been inserted into the database", "countersData": countersResponse['response']}
        except:
            logging.critical(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " Failed to enter the the data into the database")
            return {"success": False, "response": "Failed to enter the the data into the database"}

    else:
        return countersResponse


try:
    while 1:
        for server in serverList:
            hostname = server['hostname']
            port = server['port']
            request = "getAll"
            print(getCounters(hostname, port, request))
            time.sleep(2)
        time.sleep(60)
except KeyboardInterrupt:
    pass



conn.close()