from sqlite3 import Error
import argparse
import sqlite3
import sys
import re

parser = argparse.ArgumentParser(description='Query the nmap scan database instead of using the web interface')
parser.add_argument('-c', type=str, help='The columns to return, comma separated',default="*")
parser.add_argument('-d', type=str, help='The database file to use',default='app/scanned.db')
parser.add_argument('-p', type=str, help='The ports to return, comma separated',default="%")
parser.add_argument('-e', help='Just print the table column headers', action='store_true')
parser.add_argument('-s', type=str, help='Specify the ouput separator',default=",")
parser.add_argument('-t', type=str, help='The database table',default="targets")
args = parser.parse_args()

def create_connection(database):
    """ Connects to the database file """
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)

    return None

def get_db_cols(conn, table):
    """ Create a table in the database """
    query = f"PRAGMA table_info({table});"
    try:
        c = conn.cursor()
        c.execute(query)
        return c.fetchall()
    except Error as e:
        print(e)
        exit(1)


def query_db(conn, columns, table, ports):
    """ Create a table in the database """
    queryPorts = ' AND ports LIKE '.join(['"%|'+str(port)+'|%"' for port in ports])
    query = f"SELECT {columns} from {table} WHERE ports LIKE {queryPorts}"
    try:
        c = conn.cursor()
        c.execute(query)
        return c.fetchall()
    except Error as e:
        print(e)
        exit(1)

def main():

  conn = create_connection(args.d)

  if args.e:
      rows = get_db_cols(conn, args.t)
      print(f'{args.s}'.join([row[1] for row in rows]))
      exit()

  rows = query_db(conn, args.c, args.t, args.p.split(","))
  for row in rows:
      print(f'{args.s}'.join([str(item) for item in row]))

if __name__ == '__main__':
    main()