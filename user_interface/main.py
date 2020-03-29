# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:06:02 2020

@author: jairp
"""

################################################################################

### 1. Imports 

import os
import re
import sys
import time
import argparse 
from util import query_executer
from useroptions import LoginSession
from customer import CustomerSession 
from manager import ManagerSession 
from mate import MateSession
from admin import MasterSession 
from getpass import getpass
from visualizations import visualizations_menu

# other
EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+'
STRONG_EMAIL = r'[A-Za-z0-9@#$%^&+=]{8,}'

###############################################################################

### 2. Application arguments setup 

description = """Application to interact with the mate rental database.
                Please choose one of the options displayed."""

parser = argparse.ArgumentParser(description=description) 
parser.add_argument("--option",help="Run input command number")
parser.add_argument("--arg1", help="Argument 1") # argument accepting input path 
parser.add_argument("--boolarg1",help="Boolean argument, stores boolean", 
                    action="store_true")
parser.add_argument("--verbose", help="Display more information")
parser.add_argument("--demo", help="Run a demo")
args = parser.parse_args() # obtain arguments 

###############################################################################

### 3. Driver script

if __name__ == '__main__': 
    
    # Options pased as arguments by command line 
    if args.option: 
        print("Chosen option = ", args.option)
    if args.demo: 
        print("Running demo...")
        
    # Variables to be used by options: 
    login = {} 
    master_tries = 3
        
    ## LOGIN LOOP ## 
    while True: 
        
        login_string = "\n######################################################\n"
        login_string += "Welcome to the MateRental database! \n"
        login_string += "######################################################\n"
        login_string += "\nPlease choose one of the available options below:\n"
        login_string += "\t 1. Log-in\n"
        login_string += "\t 2. Register\n"
        login_string += "\t 3. Administrator Connection\n"
        login_string += "\t 4. Visualizations menu " 
        login_string += "\t 5. Exit"
        print(login_string) 
        
        try: 
            # Prompt and parse input
            user_input = input() 
            
            ## 1. Log-in menu 
            if re.match(r'^1.*', str(user_input)): 
                
                # fetch username 
                user = input("Username or email: ") 
                password = getpass() # obtain screen encrypted password
                logses = LoginSession() # instantiate object
                login = logses.login(user=user, password=password) # this will return all login info
                
                # If login was successful
                if login['login_status'] == True: 
                    print("Successful login!")
                    print("Login response: \n", login, "\n")
                    logses.fetch_usertype() # retrieve values for usertype
                    print("Usertype values: \n", logses.usertype_vals)  
                    
                    if logses.usertype == 'manager': 
                        print("\n******MANAGER ACESS******\n")
                        mgr_access = ManagerSession(logses) # initialize and copy attributes.  
                        
                    elif logses.usertype == 'mate': 
                        print("\n******MATE ACESS******\n")
                        mate_access = MateSession(logses) # initialize and copy attributes.  
                        
                    elif logses.usertype == 'customer': 
                        print("\n******CUSTOMER ACESS******\n")
                        cust_access = CustomerSession(logses) # initialize and copy attributes.   
                        
                    else: 
                        raise TypeError("Usertype not existent.")

            elif re.match(r'^2.*', str(user_input)):
                
                logses = LoginSession()  # initialize session  
                logses.newuser() # create new user
                
                

            elif re.match(r'^3.*', str(user_input)) and master_tries > 0: 
                password = getpass("Administrator password:") 
                if password == 'Jiaozics421g88-': 
                    print("******ADMIN ACESS******\n")
                    admin_access =  MasterSession() # initialize full-access session 
                else:
                    print("Wrong password")
                    master_tries -= 1
                    print("Tries left: {}".format(master_tries))
                    if master_tries == 0: 
                        print("WARNING: Administrator access deactivated")
                        
            elif re.match(r'^5.*', str(user_input)):
                visualizations_menu() # Call the visualizations menu 
            
            elif re.match(r'^5.*', str(user_input)):
                print("~Goodbye~")
                sys.exit()
            else: 
                print("Invalid input") 
                
                
            ## 2. Options menu for customer: 
            
                
        except Exception as e: 
            print("I/O error occurred\n")
            print("ARGS:{}\n".format(e.args))
            print("Error: ", e)
            print(e.__traceback__)
            print("Context: ", e.__context__)





