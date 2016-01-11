# Scripting2Eindopdracht

Welkom op de github pagina van Scripting 2, de Eindopdracht.
Deze repository bestaat uit twee delen, een management kant met een management script die de agents polled. En de resultaten opslaat in een sqlite database. Op deze management machina zal ook een webbrowser draaien welke via CGI python scipts uitvoert om de data te weergeven.
Het tweede deel zijn de agent scripts. Deze agent scripts kunnen informatie uit het systeem halen, de zogenoemde counters. Deze counters worden in windows via powershell opgevraagd en in linux via python modules of linux bestanden. Deze data wordt via een RAW tcp socket overgestuurd waarbij de informatie in JSON wordt verstuurd.

## Management

Management beschikt over de volgende bestanden:
-   management.py (Het polling script welke de data in sqlite zet)
-   networkmonitoring.db (de sqlite db)
-   removeServer.py (Hiermee kunnen agents uit de DB worden verwijderd)
-   insertServer.py (Hiermee kunnen agents in de DB worden toegevoegd)
-   management.log (Log messages van management.py worden hierin opgeslagen)
-   cgi/csvreader.py (De web pagina welke de data uit sqlite omzet naar CSV)
-   cgi/history.py (Laat de laatste 1000 entries zien door het managementscript)
-   cgi/index.py (Leest alle counters uit voor alle agents en laat dit op verschillende manieren zien)
-   cgi/footer.html (Statische HTML voor het uiterlijk van de web pagina en wat JQUERY scripts)
-   cgi/navbar.html (Statische HTML voor het uiterlijk van de web pagina)


## Agent

-   agent.py (de agent service welke een socket server opent voor TCP verbindingen, vraagt de counters op uit het systeem)
-   agent.log (Log messages gegenereerd door agent.py worden hierin opgeslagen)
-   config.xml (De agent config is hierin opgeslagen, hier wordt de authenticatie token, server poort en address in gedefinieerd)
-   windowsCounters.ps1 (In het geval van een windows systeem zal deze door agent.py worden uitgevoerd voor de performance counters)


LINUX
Install:

apt-get install python3 python3-pip
pip3 install netifaces
pip3 install psutil
