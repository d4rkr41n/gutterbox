import sys
import nmap
# initialize the port scanner
nmScan = nmap.PortScanner()

# scan localhost for ports in range 21-443
nmScan.scan('127.0.0.1', '21-443')

# run a loop to print all the found result about the ports
for host in nmScan.all_hosts():
    sys.stdout.write("{};{};{};".format(host, nmScan[host].hostname(), nmScan[host].state()) )
    for proto in nmScan[host].all_protocols():
        sys.stdout.write("{};".format(proto))
        lport = nmScan[host][proto].keys()
        lport = sorted(lport)
        for port in lport:
            sys.stdout.write("{};{};".format(port, nmScan[host][proto][port]['state']))
    sys.stdout.write("\n")
