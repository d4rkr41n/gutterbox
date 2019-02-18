from sqlite3 import Error
import sqlite3
import sys
import re

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
    database = 'scanned.db'

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

    add_item(conn, "windows", "localhost", 1, "80,69,8080")

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    main()
