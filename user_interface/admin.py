# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 19:43:05 2020

@author: jairp
"""

import re
from util import query_executer
from login import LoginSession
           
################################################################################3
    
class MasterSession(LoginSession):
    """ 
    This child class allows for more flexible and general queries including custom queries. 
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
                print("Please input any SQL query (query will be submitted when ; is entered) ") 
                
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
                
                
    def master_query(self): 
        """
        Prompts a general query to the user and attempts to execute it. 
        """
        
        while True: 
            menu_string = "\n######################################################\n"
            menu_string += "                     Custom Query                      \n"
            menu_string += "######################################################\n"
            menu_string += "\nPlease select eh type of custom query you intend to input:\n"
            menu_string += "\t 1. SELECTION query\n"  
            menu_string += "\t 2. INSERT/UPDATE/DELETE query\n"
            menu_string += "\t 3. Exit"
            print(menu_string) 
            
            mgr_input = input() 
            
            if re.match(r'^1.*', str(mgr_input)): 
                stmt = input("Please type your query:") 
                query_executer(stmt)
                
            elif re.match(r'^2.*', str(mgr_input)): 
                stmt = input("Please type your query") 
                query_executer(stmt) 
            
            elif re.match(r'^3.*', str(mgr_input)): 
                print("Exiting...")
                break
            else: 
                print("Invalid Input")
        
        return
