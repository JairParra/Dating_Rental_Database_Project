#!/usr/bin/python 

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 20:58:07 2020

@author: jairp

Connection script to Postgres SQL database 

""" 

import psycopg2 
import pandas as pd
from config import config 


def connect(): 
    """ Connect to the PosgreSQL database server """
    
    # connection variable 
    conn = None
    fetched_df = pd.DataFrame() 
    
    try: 
        # read connection parameters 
        params = config()
        
        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...") 
        conn = psycopg2.connect(**params) 
        
        # create a cursor 
        cur = conn.cursor()
        
        # execute a statement 
        print('PostgreSQL database version: ') 
        cur.execute('SELECT version();') 
        
        # display the PostgreSQL database version 
        db_version = cur.fetchone()
        print(db_version)
        print("type(fetchone) : ", type(db_version))
        
        # fetch some more stuff
        print("SELECT * FROM application;\n") 
        cur.execute("SELECT * FROM application WHERE matename='fefefe' LIMIT 20;")
        
        # display the results
        competition = cur.fetchall() 
        for row in competition: 
            print(row)
            
            
        columns = [desc[0] for desc in cur.description] 
        fetched_df = pd.DataFrame(competition, columns=columns)
        if len(fetched_df) == 0 : 
            print("EMPTY!")
                
        print("type(fetchall) : ", type(competition))
        
        print("\nOutput query: \n", fetched_df)
        
        # close the communication with the PostgreSQL 
        cur.close() 
        
    except (Exception, psycopg2.DatabaseError) as error: 
        print(error) 
        
    finally: 
        # verify connection is not empty 
        if conn is not None:  
            conn.close() 
            print("\n Database connection closed. ")
            
    return fetched_df
            
            
if __name__ == '__main__': 
    
    fetched_df = connect() 
    
    
            
