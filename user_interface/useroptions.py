# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:44:21 2020

@author: jairp
"""

import os
import re
import sys
import time
import argparse 
import psycopg2  # library to connect 
import pandas as pd 
from config import config 


def login(user="", password=""): 
    """
    Validates user log-in credentials in the database. 
    @args: 
        @ user: might be the user's username or email 
        @ password: user's password
    """ 
    
    print("Logging in...") 
    login_resp = {} # a dictionary to store the response
    login_resp['status'] = False
    conn = None # connection variable 
    
    try: 
        # read connection parameters 
        params = config()
        
        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...") 
        conn = psycopg2.connect(**params) 
        
        # create a cursor 
        cur = conn.cursor()
        
        # execute a statement 
        print('Fetcing user credentials... ') 
        stmt = "SELECT * FROM usertable "
        stmt += "WHERE username='{}' OR email='{}'".format(user,user)
        stmt += "\n;"
        cur.execute(stmt) 
        
        # display the resuls
        fetcheduser = cur.fetchone()
        
        if password not in fetcheduser: 
            print("Uncorrect login") 
            cur.close()
            conn.close() 
        else:
            print("USER=\n", fetcheduser)
            
            # close the communication with the PostgreSQL 
            cur.close() 
        
    except (Exception, psycopg2.DatabaseError) as error: 
        print(error) 
        
    finally: 
        # verify connection is not empty 
        if conn is not None:  
            conn.close() 
            print("\nDatabase connection closed.\n ")
                
    
    return login_resp 