# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 19:26:11 2020

@author: jairp
"""

import re
from util import query_executer
from login import LoginSession


################################################################################

### Class definition ### 
        
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