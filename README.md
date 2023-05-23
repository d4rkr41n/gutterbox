# Gutterbox
This tool was intened to make looking at large nmap scans easier.

## Importing Scans
Gutterbox currently loosly supports xml nmap scans. Suggested usage is as follows...
```bash
nmap -O -oX scan.xml 192.168.1.0/24
```
After the scan has been completed, the parse must be ran to convert the xml to sqlite3...
```bash
python3 parser.py -x scan.xml
```

## Using the tool
Really the meat and potatoes is that you now have an sqlite3 file! So fun! There is also a super powerful hyper intesive webserver that can view the database easier...
```bash
python3 run.py
```

## Contributing
Yeah, so this tool isn't the best right now. My original intention was to make an easy way to filter nmap scans and that didn't exist when this was first created. This also allows output to be concatenated. So maybe multiple scans are ran at once and then all the output files could be imported with...
```bash
for i in *.xml;do python3 parser.py -x $i;done
```
With that spirit in mind, feel free to contribute! There are a lot of things that need fixing and updating for this project and I don't mind the help or feature ideas!
