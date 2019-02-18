NMAP_FILE="scant"

egrep -v "^#|Status: Up" $NMAP_FILE | cut -d' ' -f2 -f4- | \
sed -n -e 's/Ignored.*//p' | \
awk -F, '{split($0,a," "); printf "Host: %-20s Ports Open: %d\n" , a[1], NF}' \
| sort -k 5 -g
