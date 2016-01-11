__author__ = 'marco'
import asyncio
import json
import os
import subprocess
from datetime import timedelta
import netifaces as ni
import psutil
import xml.etree.ElementTree as ET
import logging
logging.basicConfig(filename='agent.log',level=logging.DEBUG)

# get config
tree = ET.parse('config.xml')
serverConfig = tree.getroot()
bindAddress = serverConfig.find("hostName").text
authToken = serverConfig.find("authToken").text
bindPort = int(serverConfig.find("port").text)
osName = os.name


class ServerAgent(asyncio.Protocol):
    def connection_made(self, transport):
        """Called when a connection is made.

        The argument is the transport representing the pipe connection.
        To receive data, wait for data_received() calls.
        When the connection is closed, connection_lost() is called.
        """

        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        """Called when some data is received.

        The argument is a bytes object.
        """

        global authToken
        try:
            message = data.decode("utf-8")
        except UnicodeDecodeError:
            # if for example telnet opens to this port, it will throw this error
            logging.warning("Received a connection with an unsported protocol for exampole telnet from: " + self.transport.get_extra_info('peername'))
            self.transport.close()
            return
        # Removes line endings for clients using putty etc... (Mainly for testing)
        message = message.replace("\r", "")
        message = message.replace("\n", "")
        # Prints received data in console
        logging.info("Received request: " + message)
        print('Data received: {!r}'.format(message))
        try:
            # Parse message to JSON object
            jsonMessage = json.loads(message)
        except:
            if message == "":
                self.transport.write('{"success": false, "response": "Empty message received"}\n'.encode("utf-8"))
            else:
                self.transport.write('{"success": false, "response": "Invalid JSON received"}\n'.encode("utf-8"))
        else:
            # We need a request before knowing what to do, checking if we got that...
            if "token" not in jsonMessage.keys():
                logging.warning("Missing authentication token from client: " + self.transport.get_extra_info('peername'))
                self.transport.write('{"success": false, "response": "Missing authentication token in JSON"}\n'.encode("utf-8"))
            elif jsonMessage['token'] == authToken:
                if "request" not in jsonMessage.keys():
                    self.transport.write('{"success": false, "response": "Missing request in JSON"}\n'.encode("utf-8"))
                    logging.warning("Missing request field in json from: " + self.transport.get_extra_info('peername'))
                else:
                    if jsonMessage['request'] == "getAll":
                        # do stuff to collect counters and parse them to json and send
                        self.getAll()
                    elif jsonMessage['request'] == "multiple":
                        # This is an example call that could easily be added
                        # find the array with which counters we should send for example
                        self.transport.write('{"success": false, "response": "This request is not yet supported"}\n'.encode("utf-8"))
                    else:
                        self.transport.write('{"success": false, "response": "Invalid request"}\n'.encode("utf-8"))
                        logging.warning("Received a invalid request from: " + self.transport.get_extra_info('peername'))
            else:
                self.transport.write('{"success": false, "response": "Authentication token is incorrect, access denied."}\n'.encode("utf-8"))
                logging.warning("Invalid authentication token from: " + self.transport.get_extra_info('peername'))


    def getPowershell(self):
        """Called when the counters need to be retrieved from PS

        returns a dictionary
        """
        currentWorkingDir = os.getcwd()
        p=subprocess.Popen(['powershell.exe',
           '-ExecutionPolicy', 'Unrestricted',
           '-File', '' + currentWorkingDir + '/windowsCounters.ps1'],
            stdout = subprocess.PIPE)
        output = p.stdout.read()
        output = output.decode("utf-8")
        output = output.replace("\n", "")
        try:
            outputObject = {"success": True, "response": json.loads(output)}
        except:
            outputObject = {"success": False, "response": "Could not get information from powershell counters"}
        return(outputObject)

    def getAll(self):
        """Called when all counters available need to be retrieved

        response with jsonstring to the requester over TCP
        """
        if osName == "posix":
            # Get process count
            pidList = []
            for pid in os.listdir('/proc'):
                if pid.isdigit():
                    pidList.append(pid)

            # get system uptime
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime_string = str(timedelta(seconds = uptime_seconds))

            # Get system ip addresses
            ips = []
            for interface in ni.interfaces():
                ips.append(ni.ifaddresses(interface)[2][0]['addr'])

            # get system diskspace
            statvfs = os.statvfs('/')
            diskSize = str((statvfs.f_frsize * statvfs.f_blocks) / (1024 * 1024))
            diskAvailable = str((statvfs.f_frsize * statvfs.f_bavail) / (1024 * 1024))
            diskInfo = {"size": diskSize, "free": diskAvailable}

            # get memory information
            vmemObject = psutil.virtual_memory()
            memoryTotal = str(vmemObject.total / (1024 * 1024))
            memoryAvailable = str(vmemObject.available / (1024 * 1024))
            memInfo = {"totalMem": memoryTotal, "freeMem": memoryAvailable}

            # get cpu ussage
            cpuPercent = str(psutil.cpu_percent())

            # build the response object
            responseDict = {"proccount": len(pidList), "os": "Linux", "uptime": uptime_string, "ips": ips, "disk": diskInfo, "memory": memInfo, "cpuUssage": cpuPercent}
            response = {"success": True, "response": responseDict}
            # convert to json string
            response = json.dumps(response)
            #send to the client
            self.transport.write((response + "\n").encode("utf-8"))

        elif osName == "nt":
            #get the powershell values
            messageObject = self.getPowershell()

            #set OS type
            messageObject['response']['os'] = "Windows"

            #add cpu from psutil
            messageObject['response']['cpuUssage'] = str(psutil.cpu_percent())

            self.transport.write((json.dumps(messageObject) + "\n").encode("utf-8"))
        else:
            self.transport.write('{"success": false, "response": "This request is not supported on this OS"}\n'.encode("utf-8"))

# create a asynchronous loop
loop = asyncio.get_event_loop()
# Each client connection will a new instance of class ServerAgent, this will allow multiple clients at the same time
try:
    coro = loop.create_server(ServerAgent, bindAddress, bindPort)
except:
    print("could not start server, port in use")
    logging.critical("COULD NOT START SERVER, PORT 8888 IN USE. PLEASE CLOSE DOWN ANY PROGRAMS THAT MIGHT USE THIS PORT")
    quit()
server = loop.run_until_complete(coro)

# Serve requests until canceled
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()