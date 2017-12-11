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
    #to MSD on AWS. track_metadata.db probably needs a path unless in same folder
    cur.execture("ATTACH DATABASE 'track_metadata.db' AS db1;")
    cur.execute("SELECT * FROM lyrics JOIN db1 ON lyrics.track_id =db1.TABLENAME.track_id WHERE db1.TABLENAME.year IS NOT NULL;")
    
    rows = cur.fetchall()
    
    for row in rows
        print(row)
    
def main():
#put path to lyricdb on AWS here
    database = "C:\\sqlite\db\pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        select_all_songs(conn)
 
 
 
if __name__ == '__main__':
    main()