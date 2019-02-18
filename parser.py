import xml.etree.ElementTree as ET
from sqlite3 import Error
import argparse
import sqlite3
import sys
import re


parser = argparse.ArgumentParser(description='Convert your nmap scans into a sqlite database!')
parser.add_argument('-d', type=str, help='The database file to use',default='scanned.db')
parser.add_argument('-x', type=str, help='The xml file to read from, please use -oX with nmap')
args = parser.parse_args()


if(args.d == None or args.x == None):
    raise("Must have a database and xml file!")


class target:
    def __init__(self, os,hostname,address,ports):
        self.os = os
        self.hostname = hostname
        self.address = address
        self.ports = ports

    def ptarg(self):
        print("{}\n{}\n{}\n{}\n".format(self.os,self.hostname,self.address,self.ports))

    def add(self,conn):
        add_item(conn,self.os,self.hostname,self.address,self.ports)


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

def add_item(conn, os, hostname, address, ports):
    """ Create a table in the database """
    values = (os,hostname,address,ports)
    query = """ INSERT into targets (os,hostname,address,ports)
                VALUES(?,?,?,?); """
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

    """ Create the table if it isn't there """
    targetTableCreate = """ CREATE TABLE IF NOT EXISTS targets (
                                id integer PRIMARY KEY,
                                os text,
                                hostname text,
                                address integer,
                                ports text
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

        for o in host.iter('osclass'):
            os = str(o.attrib['osfamily'])

        for hm in host.iter('hostname'):
            hostname = str(hm.attrib['name'])

        for addr in host.iter('address'):
            if(addr.attrib['addrtype'] == 'ipv4'):
                address = str(addr.attrib['addr']).split('.')[-1]

        for port in host.iter('port'):
                ports.append(str(port.attrib['portid']))



        targets.append(target(os, hostname, address, ', '.join(ports)))
    # Write the targets to the database
    for tar in targets:
        tar.add(conn)

    # Close the database connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
