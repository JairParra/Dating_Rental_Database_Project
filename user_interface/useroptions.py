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
import psycopg2  # library to connect 
import pandas as pd 
from config import config 

###############################################################################

### 2. Main Class ### 

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
        
###############################################################################

### 3. Children Classes ### 
        
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
        
        self.menu() # display appropriate optins menu
        
        
    def menu(self): 
        """
        Customized Menu with Manager Options
        """ 
        
        while True: 
            menu_string = "\n######################################################\n"
            menu_string += "                     Options Menu                      \n"
            menu_string += "######################################################\n"
            menu_string += "\nPlease choose one of the available options below:\n"
            menu_string += "\t 1. Review Mate Application\n"  
            menu_string += "\t 2. Modify Order\n"
            menu_string += "\t 3. Overview Activity"
            menu_string += "\t 4. Exit"
            print(menu_string) 
            
            mgr_input = input() 
            
            if re.match(r'^1.*', str(mgr_input)): 
                print("Review application") 
                
            elif re.match(r'^2.*', str(mgr_input)): 
                print("Modify Order")
            
            elif re.match(r'^3.*', str(mgr_input)): 
                print("Overview Activity")
                
            elif re.match(r'^4.*', str(mgr_input)): 
                print("Exiting...")
                break
            else: 
                print("Invalid Input")
            
        
        
        
class MateSession(LoginSession):
    """ 
    Inherits from the LoginSession class and implements extra methods
    appropriate to Mate Functions and permissions. 
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
                
        print("MATE LOGIN: \n", self.login_resp) 
        print("MATE TYPE: \n", self.usertype)
        print("MATE VALUES: \n", self.usertype_vals)
        
        self.menu() # display appropriate options menu 
        
        
    def menu(self): 
        """
        Customized Menu with Mate Options
        """ 
        
        while True: 
            menu_string = "\n######################################################\n"
            menu_string += "                     Options Menu                      \n"
            menu_string += "######################################################\n"
            menu_string += "\nPlease choose one of the available options below:\n"
            menu_string += "\t 1. Apply to be a Mate\n"  
            menu_string += "\t 2. Decide on Request\n"
            menu_string += "\t 3. Modify profile" # a Mate can edit it's ownprofile 
            menu_string += "\t 4. Exit"
            print(menu_string) 
            
            mgr_input = input() 
            
            if re.match(r'^1.*', str(mgr_input)): 
                print("Apply to be a mate") 
                
            elif re.match(r'^2.*', str(mgr_input)): 
                print("Decide request")
            
            elif re.match(r'^3.*', str(mgr_input)): 
                print("Modify profile")
                
            elif re.match(r'^4.*', str(mgr_input)): 
                print("Exiting...")
                break
            else: 
                print("Invalid Input")
  

    
class CustomerSession(LoginSession):
    """ 
    Inherits from the LoginSession class and implements extra methods
    appropriate to Customer Functions and permissions. 
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
                
        print("CUSTOMER LOGIN: \n", self.login_resp) 
        print("CUSTOMER TYPE: \n", self.usertype)
        print("CUSTOMER VALUES: \n", self.usertype_vals)
        
        self.menu() # display appropriate options menu 
        
        
    def menu(self): 
        """
        Customized Menu with Customer Options
        """ 
        
        while True: 
            menu_string = "\n######################################################\n"
            menu_string += "                  Customer Options Menu                 \n"
            menu_string += "######################################################\n"
            menu_string += "\nPlease choose one of the available options below:\n"
            menu_string += "\t 1. See Mates\n" # will have a sub menu to see available mates --> extra menu, new order 
            menu_string += "\t 2. See my orders\n" # will have an option to : Modify order, cancel order
            menu_string += "\t 3. Rate Order\n"
            menu_string += "\t 4. Pay Invoice\n"
            menu_string += "\t 5. Update preferences\n"
            menu_string += "\t 6. Exit\n"
            print(menu_string) 
            
            mgr_input = input() 
            
            if re.match(r'^1.*', str(mgr_input)): 
                self.see_mates() 
                
            elif re.match(r'^2.*', str(mgr_input)): 
                print("See my orders")
            
            elif re.match(r'^3.*', str(mgr_input)): 
                print("Rate Order")
                
            elif re.match(r'^4.*', str(mgr_input)): 
                print("Pay Invoice")
                
            elif re.match(r'^5.*', str(mgr_input)): 
                print("Update preferences")
                
            elif re.match(r'^6.*', str(mgr_input)): 
                print("Exit")
                break
            else: 
                print("Invalid Input")
                
    
    def see_mates(self): 
        """
        Function for menu option 1. 
        """
        
        try: 
            
            while True: 
                menu_string = "\n######################################################\n"
                menu_string += "                    Look for a Mate                   \n"
                menu_string += "######################################################\n"
                menu_string += "1. See all mates\n"
                menu_string += "2. Custom search\n" 
                menu_string += "3. Exit\n"
                print(menu_string)
                
                sub_input1 = input() 
                
                if re.match(r'^1', str(sub_input1)): 
                    
                    ## 1.7 Order by 
                    print("**Order by**")
                    print("1.Hourly Rate \n2.Age \n3.Nickname \n4.None") 
                    if re.match(r'^1', str(input())): 
                        order = "hourlyrate" 
                    elif re.match(r'^2', str(input())):
                        order = "age" 
                    elif re.match(r'^3', str(input())):
                        order = "nickname"
                    elif re.match(r'^3', str(input())):
                        order = None
                    else: 
                        print("Invalid input") 
                        continue
                    
                    stmt = "SELECT nickname,\n\t description\n\t, sex,\n\t language,\n\t height,\n\t weight,\n\t hourlyrate \n" 
                    stmt += "FROM mate m \n"
                    stmt += "JOIN usertable u \n"
                    stmt += "\t ON m.username = u.username \n"
                    if order is not None: 
                        stmt += "ORDER BY {}\n".format(order)
                    stmt += ";\n"     
                    
                    query_executer(stmt) # execute and display query and result 
                    
                elif re.match(r'^2', str(sub_input1)):
                    
                    ## 1. Custom search according to different attributes
                    print("Custom search: Choose custom preferences for your mate :) ") 
    
                    ### 1.1 Sex
                    print("Sex:\n 1) Male 2)Female") 
                    if re.match(r'^1', str(input())):
                        sex = "Male"
                    elif re.match(r'^2', str(sub_input1)): 
                        sex = "Female"
                    else: 
                        print("Invalid input") 
                        continue
                    
                    ### 1.2. Age
                    print("**Age**")
                    lower_age = input("Min: ") 
                    upper_age = input("Max: ")
                    if lower_age < 18: 
                        print("I'm calling the police...")
                        raise ValueError("WARNING: Pedophile spotted")
                        break
                    
                    ### 1.3 Languages
                    print("**Languages spoken:**")
                    print("1) English \n2) French\n3) Both")
                    if re.match(r'^1', str(input())): 
                        lang = "English" 
                    elif re.match(r'^2', str(input())):
                        lang = "French" 
                    elif re.match(r'^3', str(input())):
                        lang = "Eng & French"
                    else: 
                        print("Invalid input") 
                        continue
                    
                    ## 1.4 Height
                    print("**Height (cm)**")
                    lower_height = float(input("Min: "))/100
                    upper_height = float(input("Max: "))/100 
                    if lower_height > upper_height: 
                        print("Invalid input")
                        continue
                    
                    ## 1.5 Weight 
                    print("**Weight (kg)**")
                    lower_weight = int(input("Min: ")) 
                    upper_weight = int(input("Max: ")) 
                    if lower_weight > upper_weight: 
                        print("Invalid input")
                        continue
                    
                    ## 1.6 Hourly Rate 
                    print("**Hourly rate (CAD$)**") 
                    lower_rate = int(input("Min: "))
                    upper_rate = int(input("Max: "))
                    if lower_rate > upper_rate: 
                        print("Invalid input")
                        continue
                    
                    ## 1.7 Order by 
                    print("**Order by**")
                    print("1.Hourly Rate \n2.Age \n3.Nickname") 
                    if re.match(r'^1', str(input())): 
                        order = "hourlyrate" 
                    elif re.match(r'^2', str(input())):
                        order = "age" 
                    elif re.match(r'^3', str(input())):
                        order = "nickname"
                    else: 
                        print("Invalid input") 
                        continue
                    
                    stmt = "SELECT * FROM "
                    stmt += "\t ("
                    stmt = "\t SELECT \n"
                    stmt += "\t\t m.nickname, \n"
                    stmt += "\t\t u.sex,\n"
                    stmt += "\t\t DATE_PART('year', CURRENT_DATE) - DATE_PART('year', u.dateofbirth) AS age,\n"
                    stmt += "\t\t m.language,\n"
                    stmt += "\t\t m.height,\n"
                    stmt += "\t\t m.weight,\n" 
                    stmt += "\t\t m.hourlyrate,\n" 
                    stmt += "\t\t m.description\n"
                    stmt += "\t FROM mate m \n" 
                    stmt += "\t JOIN usertable u \n"
                    stmt += "\t\t ON m.username = u.username"
                    stmt += "\t WHERE sex='{}' AND language='{}' \n".format(sex,lang)
                    stmt += "\t\t AND (height BETWEEN {} AND {}) \n".format(lower_height, upper_height) 
                    stmt += "\t\t AND (weight BETWEEN {} AND {}) \n".format(lower_weight, upper_weight) 
                    stmt += "\t\t AND (hourlyrate BETWEEN {} AND {}) \n".format(lower_rate, upper_rate) 
                    stmt += "\t ORDER BY '{}' \n".format(order) 
                    stmt += "\t ) T"
                    stmt += "WHERE T.age BETWEEN {} AND {}".format(lower_age, upper_age)
                    stmt += ";\n" 
                    
                 
                elif re.match(r'^3', str(sub_input1)): 
                    print("Exit")
                    break
                else: 
                    print("Invalid Input")
                    
        except Exception as e: 
            print("I/O error occurred\n")
            print("ARGS:{}\n".format(e.args))
            print("Error: ", e)
            print(e.__traceback__)
            print("Context: ", e.__context__)
                        
                        
    
    
class MasterSession(LoginSession):
    """ 
    This allows for special 
    """ 
    def __init__(self, verbose=True): 
        """
        @args: 
            @ loginsession: an instance of the LoginSession class. Will throw an error 
            if wrong type input. 
        """
        # Initialize and typecheck
        super().__init__(verbose) # call super constructor 
#        if not isinstance(loginsession, LoginSession):
#            raise TypeError("Constructor argument should be of type 'LoginSession'")
            
        # Copy all attributes from argument instance
        self.login_resp = None
        self.usertype = "Master/Admin"
        self.usertype_vals = None
                
        print("LOGIN: \n", self.login_resp) 
        print("TYPE: \n", self.usertype)
        print("VALUES: \n", self.usertype_vals)
        
        self.menu() # display appropriate options menu 
        
        
    def menu(self): 
        """
        Master menu
        """ 
        
        while True: 
            menu_string = "\n######################################################\n"
            menu_string += "                     Options Menu                      \n"
            menu_string += "######################################################\n"
            menu_string += "\nPlease choose one of the available options below:\n"
            menu_string += "\t 1. Master Query \n" # will have a sub menu to see available mates --> extra menu, new order 
            menu_string += "\t 2. See/modify Users \n" 
            menu_string += "\t 3. See/modify Managers \n" 
            menu_string += "\t 4. See/modify Mates \n" 
            menu_string += "\t 5. See/modify Customers \n"
            menu_string += "\t 6. See/modify mate Requests \n" 
            menu_string += "\t 7. See/modify Orders (of mate Requests) \n" # table
            menu_string += "\t 8. See/modify Invoices (of Orders) \n" 
            menu_string += "\t 9. See/modify placed requests and dates \n" # table = <startdate>
            menu_string += "\t 10. See/modify Order generations \n" #  table = <generate>
            menu_string += "\t 11. See/modify Manager Modifications \n" 
            menu_string += "\t 12. See/modify Scheduled activities \n"
            menu_string += "\t 13. Exit \n"
            print(menu_string) 
            
            mgr_input = input() 
        
            if re.match(r'^1[^0-3]+|^1$', str(mgr_input)): 
                print("Please input any SQL query: ") 
                
            elif re.match(r'^2.*', str(mgr_input)): 
                print("See/modify Users")
                
            elif re.match(r'^3.*', str(mgr_input)): 
                print("See/modify Managers")
                
            elif re.match(r'^4.*', str(mgr_input)): 
                print("See/modify Mates")
                
            elif re.match(r'^5.*', str(mgr_input)): 
                print("See/modify Customers")
                
            elif re.match(r'^6.*', str(mgr_input)): 
                print("See/modify mate Requests")
                
            elif re.match(r'^7.*', str(mgr_input)): 
                print("See/modify Orders (of mate Requests)")
                
            elif re.match(r'^8.*', str(mgr_input)): 
                print("See/modify Invoices (of Orders)")
                
            elif re.match(r'^9.*', str(mgr_input)): 
                print("See/modify placed requests and dates")

            elif re.match(r'^10.*', str(mgr_input)): 
                print("See/modify Order generations")
                
            elif re.match(r'^11.*', str(mgr_input)): 
                print("See/modify Manager Modifications")

            elif re.match(r'^12.*', str(mgr_input)): 
                print("See/modify Scheduled activities")
                
            elif re.match(r'^13.*', str(mgr_input)): 
                print("Exiting MasterSession")
                break
            else: 
                print("Invalid Input") 


################################################################################
                
### 4. Utilities ### 
                
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
            

    
   