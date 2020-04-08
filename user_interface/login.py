# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:44:21 2020

@author: jairp
"""

###############################################################################

### 1. Imports ### 

import os
import re
import sys
import time
import datetime
import psycopg2  # library to connect 
import pandas as pd 
from util import config 
from getpass import getpass
from util import query_executer # custom util class

# other
EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+'
STRONG_EMAIL = r'[A-Za-z0-9@#$%^&+=]{8,}'

###############################################################################


class LoginSession(): 
    """ 
    This parent class contains 
    """
    
    def __init__(self, newuser = True, verbose=True): 
        """
        @args: 
            @ newuser: contains logging response (user values + successful login)
            @ usertype: type of user 
            @ usertype_vals: values of the user type
        """
        self.login_resp = {} # contains logging response (user values + successful login)
        self.usertype = "" # type of user
        self.usertype_vals = {} # values of user type
        self.newuser = newuser  
        if newuser: 
            print("Initialization procedure") 
            self.new_user() # Procedure to create a new user. 
            
            
    def new_user(self):  
        """
        Creates and inserts a new user in the database
        """
        
        operating = True
        try: 
            while operating:    
                
                ### 1.Prompt values 
                
                ## 1. Prompt new username and email
                print("Register: ") 
                new_user = input("Please input username: ")
                new_email = input("Please enter your email: ")
                
                stmt = "SELECT * FROM usertable WHERE username='{}' or email='{}';".format(new_user, new_email) 
                output = query_executer(stmt, verbose=False) # there shouldn't be any users in the output 
                if len(output) > 0: 
                    print("Error: A user with the same username or email already exists.") 
                    continue
                
                ## 2. verify input email is valid
                if not re.match(EMAIL_REGEX, new_email): 
                    print("Make sure you input a valid email!")
                    continue  # go back to main menu 
                
                ## 3. protmpt and verify password
                new_pass = getpass("Please input password with 1) 1 Uppercase 2) 1 lowercase 3) at least 8 characters:\n")
                if not re.match(STRONG_EMAIL, new_pass) :
                    print("Error: Password muss contain: ")
                    print(" 1 Uppercase, 1 lowercase, at least 8 characters") 
                    continue
                
                ## 4.  prompt user first and last name
                firstname = input("First name: ")
                lastname = input("Lasname: ") 
                
                ## 5. Sex
                print("Sex:\n1. Male\n2. Female") 
                user_input = input()
                if re.match(r'^1.*', str(user_input)): 
                    sex =  "Male" 
                elif re.match(r'^2.*', str(user_input)):
                    sex = "Female" 
                else: 
                    print("Invalid input")
                    continue 
                
                ## 6. city
                city = input("City: ") 
                
                ## 7. Phonenumber
                phonenum = input("Please input your phone number with no spaces or special characters: ") 
                if not (phonenum.isdigit() and len(phonenum) > 6 and len(phonenum) < 15): 
                    print("Invalid input") 
                    
                ## 8. dateofbirth 
                print("Date of birth: ") 
                year = input("year (YYYY): ")
                month = input("month (MM): ")
                day = input("day (DD): ") 
                
                if not (year.isnumeric() and month.isnumeric() and day.isnumeric() 
                        and (int(str(datetime.date.today().year)) - int(year)) > 18 ): 
                    print("Invalid input or age: you must be at least 18 years old to use the service.") 
                    
                date = str(datetime.date(year=int(year),month=int(month),day=int(day))) 
                
                ### 2. Create statement  
                stmt = "INSERT INTO usertable (username, password, email , firstname, lastname, sex, city , phoneNum, dateOfBirth) "
                stmt += "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}') ;".format(new_user, 
                                new_pass, new_email, firstname, lastname, sex, city, phonenum, date)
                
                # Execute insertion 
                result = query_executer(stmt, insert=True) 
                
                # Verify insertion worked
                stmt = "SELECT * FROM usertable "
                stmt += "WHERE username='{}' ;\n".format(new_user)
                result = query_executer(stmt)
                
                while True: 
                    if len(result) >= 1:
                        print("--INFO-- : User succesfully created! You can now log-in.")
                        print(result) 
                        
                        sub_menu = "############################################################### \n"
                        sub_menu += "                   New User Registration                   \n"
                        sub_menu += "###############################################################\n"
                        sub_menu += "I want to register as a ...\n" 
                        sub_menu += "1. Customer\n" 
                        sub_menu += "2. Mate\n" 
                        print(sub_menu)
                        
                        user_input = input()
                        if re.match(r'^1.*', str(user_input)): 
                            self.usertype =  "Customer" 
                            preferences = input("Please write your preferences: (max 1000 characters)\n")
                            stmt = "INSERT INTO customer (username, preferences)    VALUES ('{}','{}')\n;".format(new_user, preferences)
                            query_executer(stmt,insert=True) # execute insertion. 
                            print("Thank you! You can now log-in in the main menu")
                            operating = False # finish
                            break
                        elif re.match(r'^2.*', str(user_input)):
                            self.usertype = "Mate"
                            #TODO: Implement filling infomration for a new mate
                            print("--INFO--: Information complete. You may now log-in an apply to be a mate\\")
                            print("\t\t You cannot work as a mate until a manager reviews and accepts your application.")
                            raise NotImplementedError("Functionality not available yet.")
                        else: 
                            print("Invalid input")
                            continue 
                    
                    
                else: 
                    raise ReferenceError("The record you tried to create raised an error.")
                    
                
        except Exception as e: 
            print("I/O error occurred\n")
            print("ARGS:{}\n".format(e.args))
            print("Error: ", e)
            print(e.__traceback__)
            print("Context: ", e.__context__)
            print("Cause: ", e.__cause__)


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
