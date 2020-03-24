# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 19:46:08 2020

@author: jairp
"""

###############################################################################

### 1. Imports 

import re 
import psycopg2 
import pandas as pd
from config import config 


###############################################################################

### 2. Helper Functions 

def query_executer(stmt, fetchall=True, verbose=True): 
    """
    Helper function to help executing a general quer. 
    @params: 
        @ stmt: A SQL statement. Assumed to be correct and end by a semi-colon. 
        @ fetchall: If True, return all the statements 
        @ to_df: If True, returns a dataframe of the output query
    """ 
    conn = None # Set up connection 
    
    try: 
        
        ## 1. Set up configurations
        params = config() # read connection parameters 
        conn = psycopg2.connect(**params)  # connect to the PostgreSQL server
        cur = conn.cursor() # create a cursor 
        
        ### 2. Execute query and fetch results 
        cur.execute(stmt) 
        query_colnames = [desc[0] for desc in cur.description] # fetched colnames
        query_result = cur.fetchall() # result is a list of tuples, the whole relation 
        
        ### 3. Construct dataframe if required
        output_df = pd.DataFrame(query_result, columns=query_colnames) 
            
        ### 4. Verbose: Output query and result 
        if verbose: 
            print("*****************************SQL*****************************")
            print(stmt) 
            print("***************************OUTPUT****************************")
            print(output_df)
        
        # close the communication with the PostgreSQL 
        cur.close() 
        
    except (Exception, psycopg2.DatabaseError) as error: 
        print(error) 
        
    finally: 
        # verify connection is not empty 
        if conn is not None:  
            conn.close() 
    
    # Return result
    return output_df


