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

## How to install

### Windows
- Check voor de laatste versie op: https://github.com/MarcoNijholt/Scripting2Eindopdracht en download als ZIP.
- Pak de zip uit op de gewenste locatie
- Installeer XAMPP: https://www.apachefriends.org/xampp-files/5.6.15/xampp-win32-5.6.15-1-VC11-installer.exe
- Na het installeren van xampp moet de configuratie aangepast worden voor Apache zodat deze python files als cgi uitvoert.
- vervang de huidige directory "G:/User Storage/PycharmProjects/Scripting 2 Eindopdracht/Management/cgi" door het juiste pad van waar u het project installeert in de httpd.conf file in de INSTALL directory van dit project.
- Kopieer de httpd.conf file vervolgens naar de XAMPP appache directory. (Standaard "C:\xampp\apache\conf")
- Installeer Python 3.4: https://www.python.org/downloads/release/python-344/
- Open command prompt en ga naar de python scripts folder. (Standaard C:\Python34\Scripts)
- Voer de volgende commando's uit voor het installeren van modules:
    - pip3.exe install asyncio
    - pip3.exe install psutil
    - pip3.exe install matplotlib
    - pip3.exe install pyplot
    - pip3.exe install netifaces


Nu kan je in vervolgd de python bestanden management.py voor de management server, of agent.py voor de agent servers draaien.
Om een agent toe te voegen zal die moeten worden toegevoegd aan de database. Dit kan via de insertServer.py file, verwijderen kan via removeServer.py in de management folder.

### Linux
Voer de volgende commandos uit om het op linux (debian/ubuntu) te installeren
- apt-get update
- apt-get upgrade
- apt-get install python3 python3-pip git-core python3-matplotlib apache2-mod-php5
- pip3 install netifaces
- pip3 install psutil
- git clone https://github.com/MarcoNijholt/Scripting2Eindopdracht
- Om er voor te zorgen dat apache ook de python files executeerd zal de default sites-enabled bestand moeten worden aangepast
- In /etc/apache2/sites-enabled/ zal 000-default.conf moeten worden aangepast. De volgende aanpassing zal moeten worden doorgevoerd
```bash
<Directory /var/www/Scripting2Eindopdracht/Management/cgi>
    Options +ExecCGI
    DirectoryIndex index.py
</Directory>
AddHandler cgi-script .py
DocumentRoot  /var/www/Scripting2Eindopdracht/Management/cgi
```
- Hierbij moet de directory /var/www/Scripting2Eindopdracht/Management/cgi eventueel aangepast worden naar de directory van waar u het script geplaatst heeft.

Nu kan je de python bestanden management.py voor de management server, of agent.py voor de agent servers draaien.
Om een agent toe te voegen zal die moeten worden toegevoegd aan de database. Dit kan via de insertServer.py file.

### Overzicht accociaties
![alt tag](https://raw.githubusercontent.com/MarcoNijholt/Scripting2Eindopdracht/master/INSTALL/accociaties.png)