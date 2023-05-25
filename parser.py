import xml.etree.ElementTree as ET
from sqlite3 import Error
import argparse
import sqlite3
import sys
import re


parser = argparse.ArgumentParser(description='Convert your nmap scans into a sqlite database!')
parser.add_argument('-x', type=str, help='The xml file to read from, please use -oX with nmap')
parser.add_argument('-d', type=str, help='The database file to use',default='app/scanned.db')
parser.add_argument('-i', type=str, help='The name to use for the client',default="default")
args = parser.parse_args()


if(args.d == None or args.x == None):
    raise("Must have a database and xml file!")

class target:
    def __init__(self, os,hostname,address,ports,clientId):
        self.os = os
        self.hostname = hostname
        self.address = address
        self.ports = ports
        self.clientId = clientId

    def ptarg(self):
        print("{}\n{}\n{}\n{}\n{}\n".format(self.os,self.hostname,self.address,self.ports,clientId))

    def add(self,conn):
        add_item(conn,self.os,self.hostname,self.address,self.ports,self.clientId)


def create_connection(database):
    """ Connects to the database file """
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    """ Create a table in the database """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_item(conn, os, hostname, address, ports, clientId):
    """ Create a table in the database """
    values = (os,hostname,address,ports,clientId)
    query = """ INSERT into targets (os,hostname,address,ports,clientId)
                VALUES(?,?,?,?,?); """
    try:
        c = conn.cursor()
        c.execute(query, values)
    except Error as e:
        print(e)

def main():
    """ Connect to the database file """

    database = args.d

    conn = create_connection(database)
    if conn is None:
        raise("Could not connect to database")
        exit()

    """ Create the table if it isn't there """
    targetTableCreate = """ CREATE TABLE IF NOT EXISTS targets (
                                id integer PRIMARY KEY,
                                os text,
                                hostname text,
                                address text,
                                ports text,
                                clientId text
                            ); """
    create_table(conn, targetTableCreate)


    # Start parsing the xml
    tree = ET.parse(args.x)
    root = tree.getroot()
    targets = []

    for host in root.iter('host'):
        os = None
        hostname = None
        address = None
        ports = []
        clientId = args.i

        for o in host.iter('osclass'):
            os = str(o.attrib['osfamily'])

        for hm in host.iter('hostname'):
            hostname = str(hm.attrib['name'])

        for addr in host.iter('address'):
            if(addr.attrib['addrtype'] == 'ipv4'):
                address = str(addr.attrib['addr'])

        for port in host.iter('port'):
                ports.append(str(port.attrib['portid']))

        targets.append(target(os, hostname, address, '|'+'|'.join(ports)+'|',clientId))
    # Write the targets to the database
    for tar in targets:
        tar.add(conn)
        #print(tar.ptarg())
    print(f"[*] Added {len(targets)} targets to {args.i}")

    # Close the database connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
