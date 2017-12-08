#!/usr/bin/python

import sqlite3
from sqlite3 import Error

#code from http://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None
    
    
def select_all_songs(conn):
    cur = conn.cursor()
    
    #need names of tables from MSDB and to attach them inside execute statement using path
    #to MSD on AWS 
    cur.execture("ATTACH DATABASE file_name AS db1")
    cur.execute("SELECT * FROM table")
    
    rows = cur.fetchall()
    
    for row in rows
        print(row)
    
def main():
#put path to db on AWS here
    database = "C:\\sqlite\db\pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        select_all_songs(conn)
 
 
 
if __name__ == '__main__':
    main()