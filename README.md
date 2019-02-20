# gutterbox
## setup
Install the dependancies

specify the correct version for sqlite3
```
sudo apt update
sudo apt install php libapache2-mod-php php-mysql
sudo apt install php7.0-sqlite3
```

## Use it!
Run the scan
```
nmap -O -oX /var/www/html/gutterbox/scans/scan.xml 192.168.1.0/24
```

Feed the parser
```
./parser.py -x scans/scan.xml
```
