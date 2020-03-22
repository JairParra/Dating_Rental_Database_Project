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


class LoginSession(): 
    """ 
    This parent class contains 
    """
    
    def __init__(self, verbose=True): 
        """
        @args: 
            @ login_resp: contains logging response (user values + successful login)
            @ usertype: type of user 
            @ usertype_vals: values of the user type
        """
        self.login_resp = {} # contains logging response (user values + successful login)
        self.usertype = "" # type of user
        self.usertype_vals = {} # values of user type
        if verbose: 
            print("\n*** Initializing Login ***\n")
        
        
    def login(self, user="", password="", verbose=True): 
        """
        Validates user log-in credentials in the database. 
        @args: 
            @ user: might be the user's username or email 
            @ password: user's password
            
        @returns: 
            - A dictionary object with the fetched user's information
              a boolean 'login_status' indicating whether the connection was 
              successful. 
        """ 
        
        print("Logging in...") 
        login_resp = {} # a dictionary to store the response
        login_resp['login_status'] = False # User is not logged-in by default
        conn = None # connection variable 
        
        try: 
            print("Connecting to the PostgreSQL database...")
            params = config() # read connection parameters
            conn = psycopg2.connect(**params)  # connect to the PostgreSQL server
            cur = conn.cursor() # create a cursor 
            
            # execute a statement 
            print('Fetching user credentials... ') 
            stmt = "SELECT * FROM usertable "
            stmt += "WHERE username='{}' OR email='{}'".format(user,user)
            stmt += "\n;"
            cur.execute(stmt) # execute statement
            
            # display the resuls
            fetcheduser = cur.fetchone() # single row of values 
            colnames = [desc[0] for desc in cur.description] # fetched colnames
            fetcheduser = {colnames[i]:fetcheduser[i] for i in range(len(colnames))} # pack in a dictionary
            
            # If fecheduser is empty, username doesn't exist 
            if fetcheduser is None: 
                print("ERROR: Username doesn't exist") 
                cur.close() 
                conn.close()
    
            # Validate iput password         
            if password != fetcheduser['password']: 
                print("Incorrect login") 
                cur.close()
                conn.close() 
            else:
                print("USER=\n", fetcheduser)
                login_resp.update(fetcheduser) # update response, merge both dictionaries 
                login_resp['login_status'] =  True
                
                # close the current cursor 
                cur.close() 
            
        except (Exception, psycopg2.DatabaseError) as error: 
            print("ERROR! :\n")
            print(error) # display postgresql database error 
            print("Please try again")
            
        finally: 
            # verify connection is not empty 
            if conn is not None:  
                conn.close() 
                if verbose: 
                    print("\n--INFO-- Database connection closed.\n ")
                    
        
        self.login_resp = login_resp # update login_response 
        return login_resp 
    
    
    def fetch_usertype(self, fetch_all=True, verbose=False): 
        """
        Determines usertype and fetches all the corresponding values from 
        the appropriate derived table if fetch_all==True. 
        @args: 
            @ fetch_all: retrieve all fields from the derived usertype table
        """
        conn = None 
        username = self.login_resp['username'] # fetch username
        
        try: 
            ### 1. Connection
            params = config()  # read connection parameters 
            conn = psycopg2.connect(**params) # connect to the PostgreSQL server
            cur = conn.cursor() # create a cursor 
            
            ### 2. Check for manager type
            stmt = "SELECT * FROM manager "
            stmt += "WHERE username='{}'".format(username)
            stmt += "\n;"
            cur.execute(stmt) # fetch from manager tavle
            
            fetched_manager = cur.fetchone() # single row of values 
            
            if fetched_manager is not None: 
                # update object attributes 
                print("--INFO-- User type: manager")
                self.usertype = "manager" 
                colnames = [desc[0] for desc in cur.description] 
                self.usertype_vals = {colnames[i]:fetched_manager[i] for i in range(len(colnames))}
                cur.close()  # close cursor
                conn.close() # close connection 
                return # exit
            
            ### 3. Check for mate type 
            stmt = "SELECT * FROM mate "
            stmt += "WHERE username='{}'".format(username)
            stmt += "\n;"
            cur.execute(stmt) # execute statement
            
            fetched_mate = cur.fetchone() # extract row 
            
            if fetched_mate is not None: 
                # update object attributes 
                print("--INFO-- User type: mate")
                self.usertype = "mate" 
                colnames = [desc[0] for desc in cur.description] 
                self.usertype_vals = {colnames[i]:fetched_mate[i] for i in range(len(colnames))}
                cur.close()  # close cursor
                conn.close() # close connection 
                return # exit
            
            ### 4. Check for customer type 
            stmt = "SELECT * FROM customer "
            stmt += "WHERE username='{}'".format(username)
            stmt += "\n;"
            cur.execute(stmt) # execute statement
            
            fetched_customer = cur.fetchone()
            
            if fetched_customer is not None: 
                # update object attributes 
                print("--INFO-- user type: customer")
                self.usertype = "customer" 
                colnames = [desc[0] for desc in cur.description] 
                self.usertype_vals = {colnames[i]:fetched_customer[i] for i in range(len(colnames))}
                cur.close()  # close cursor
                conn.close() # close connection 
                return # exit
            else: 
                cur.close()
                conn.close()
                raise ValueError("Invalid user type")
        
        except (Exception, psycopg2.DatabaseError) as error: 
            print("Error fetching user type :\n")
            print(error) # display postgresql database error 
            print(error.__context__)
            print(error.__traceback__)
            
        finally: 
            # verify connection is not empty 
            if conn is not None:  
                conn.close() 
                if verbose:
                    print("\n--INFO-- Database connection closed.\n ")
        
        return 
        
        
class ManagerSession(LoginSession):
    """ 
    Inherits from the LoginSession class and implements extra methods
    appropriate to Manager Functions and permissions. 
    """ 
    def __init__(self, loginsession, verbose=True): 
        """
        @args: 
            @ loginsession: an instance of the LoginSession class. Will throw an error 
            if wrong type input. 
        """
        # Initialize and typecheck
        super().__init__(verbose) # call super constructor 
        if not isinstance(loginsession, LoginSession):
            raise TypeError("Constructor argument should be of type 'LoginSession'")
            
        # Copy all attributes from argument instance
        self.login_resp = loginsession.login_resp 
        self.usertype = loginsession.usertype 
        self.usertype_vals = loginsession.usertype_vals 
                
        print("MANAGER LOGIN: \n", self.login_resp) 
        print("MANAGER TYPE: \n", self.usertype)
        print("MANAGER VALUES: \n", self.usertype_vals)
        
        
    def menu(self): 
        """
        Customized Menu with Manager Options
        """ 
        
        
    
    
    
        
        
        
