# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 19:23:34 2020

@author: jairp
"""

import re
from util import query_executer
from useroptions import LoginSession # parent class 

# other
EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+'
STRONG_EMAIL = r'[A-Za-z0-9@#$%^&+=]{8,}'

##############################################################################

### Class definition ### 
        
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

